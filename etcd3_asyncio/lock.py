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
    def __init__(self, key: bytes, *, client=None, loop=None):
        if client is None:
            client = get_client()
        if loop is None:
            loop = asyncio.get_event_loop()

        self._key = key
        self._client = client
        self._loop = loop

    def __repr__(self):
        res = super().__repr__()
        extra = 'locked' if self._locked else 'unlocked'
        return '<{} on {} [{}]>'.format(res[1:-1], self._key, extra)

    async def __aenter__(self):
        await self.acquire()
        return None

    async def __aexit__(self, exc_type, exc, tb):
        self.release()

    async def _watch(self):
        await self._client.start_session()
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

    async def acquire(self, actions=[]):
        await self._client.start_session()
        async with self._orderer:
            while True:
                lock_id = str(self._lock_id).zfill(19).encode()
                lock_key = self._session_prefix + lock_id
                self._lock_id += 1

                cond = CreateRevision(lock_key) == 0
                put = request.Put(lock_key, b'', self._client.session_id)
                get = request.Get(lock_key)
                get_owner = request.Range(self._lock_prefix, limit=1,
                                          sort_target='create',
                                          sort_order='ascend')

                success = [put, get_owner, *ensure_iter(actions)]

                succeeded, r = await request.Txn(compare=cond, success=success,
                                                 failure=[get, get_owner],
                                                 client=self._client)

                self.owner = next(iter(r[1]))

                if succeeded:
                    break
                # TODO find a good lock_id, based on newest key in session

        if self.owner != lock_key:
            fut = self._loop.create_future()
            self._waiters[lock_key] = fut
            if self._watcher is None or self._watcher.done():
                self._watcher = self._loop.create_task(self._watch())
            await fut
            _, r = await request.Txn(success=actions, client=self._client)
        return r[2:]

    async def _release(self, lock_key, actions):
        await self._client.start_session()
        actions = [request.Delete(lock_key), *ensure_iter(actions)]
        _, r = await request.Txn(success=actions, client=self._client)
        return r[1:]

    def release(self, actions=[]):
        return self._loop.create_task(self._release(self.owner, actions))

    def locked(self):
        return self.owner is not None  # TODO

    @property
    def _lock_prefix(self):
        return self._key + b'/_lock/'

    @property
    def _session_prefix(self):
        return self._lock_prefix + f'{self._client.session_id}/'.encode()

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
