'''
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
'''

import asyncio
from collections import defaultdict

from . import CreateRevision, get_client, request
from .utils import ensure_iter


class Lock():

    class _Common:
        waiters = defaultdict(dict)
        orderers = defaultdict(asyncio.Lock)
        watchers = dict()
        owners = dict()
        lock_ids = defaultdict(int)

    # TODO different loops
    def __init__(self, key: str, *, client=None, loop=None):
        if client is None:
            client = get_client()
        if loop is None:
            loop = asyncio.get_event_loop()

        self._key = key
        self._client = client
        self._loop = loop

    async def __aenter__(self):
        await self.acquire()
        return None

    async def __aexit__(self, exc_type, exc, tb):
        self.release()

    async def _watch(self):
        async for events in request.Watch(self._lock_prefix, filters='noput',
                                          client=self._client):
            owner = await request.Range(self._lock_prefix, limit=1,
                                        sort_target='create',
                                        sort_order='ascend',
                                        client=self._client)
            try:
                self.owner = next(iter(owner))
                if self.owner in self._waiters:
                    waiter = self._waiters.pop(self.owner)
                    if not waiter.done():
                        waiter.set_result(True)
                elif not self._waiters:
                    raise StopIteration
            except StopIteration:
                self.owner = None
                return
            except Exception as e:
                print('***', repr(e))
                raise

    async def acquire(self, actions=[]):
        async with self._orderer:
            while True:
                lock_id = str(self._lock_id).zfill(19)
                lock_key = self._session_prefix + lock_id
                self._lock_id += 1

                cond = CreateRevision(lock_key) == 0,
                put = request.Put(lock_key, '', self._client.session_id)
                get = request.Get(lock_key)
                get_owner = request.Range(self._lock_prefix, limit=1,
                                          sort_target='create',
                                          sort_order='ascend',
                                          client=self._client)

                actions = [put, get_owner, *ensure_iter(actions)]

                succeeded, r = await request.Txn(compare=cond, success=actions,
                                                 failure=[get, get_owner],
                                                 client=self._client)

                self.owner = next(iter(r[1]))

                if succeeded:
                    break
                # TODO find a good lock_id, based on newest key in session
                print('failed to find lock key')

        if self.owner != lock_key:
            fut = self._loop.create_future()
            self._waiters[lock_key] = fut
            if self._watcher is None or self._watcher.done():
                self._watcher = self._loop.create_task(self._watch())
            await fut
        return r[2:]

    async def _release(self, lock_key, actions):
        try:
            actions = [request.Delete(lock_key), *ensure_iter(actions)]
            _, r = await request.Txn(success=actions, client=self._client)
            return r[1:]
        except Exception as e:
            print('xxx', repr(e))

    def release(self, actions=[]):
        return self._loop.create_task(self._release(self.owner, actions))

    def locked(self):
        return self.owner is not None

    @property
    def _lock_prefix(self):
        return self._key + '/_lock/'

    @property
    def _session_prefix(self):
        return self._lock_prefix + str(self._client._session.id) + '/'

    @property
    def _orderer(self):
        return Lock._Common.orderers[self._session_prefix]

    @property
    def _watcher(self):
        return Lock._Common.watchers.get(self._session_prefix)

    @_watcher.setter
    def _watcher(self, value):
        Lock._Common.watchers[self._session_prefix] = value

    @property
    def _waiters(self):
        return Lock._Common.waiters[self._session_prefix]

    @property
    def owner(self):
        return Lock._Common.owners.get(self._lock_prefix)

    @owner.setter
    def owner(self, value):
        Lock._Common.owners[self._lock_prefix] = value

    @property
    def _lock_id(self):
        return Lock._Common.lock_ids[self._session_prefix]

    @_lock_id.setter
    def _lock_id(self, value):
        Lock._Common.lock_ids[self._session_prefix] = value
