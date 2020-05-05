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

from . import client, CreateRevision, request
from .lock import Lock
from .utils import normalize_key


class Condition(client.User):

    class _Common:
        waiters = defaultdict(dict)
        orderers = defaultdict(asyncio.Lock)
        watchers = dict()
        cond_ids = defaultdict(int)

    # TODO different loops
    def __init__(self, key: str, lock: Lock = None, *, client, loop=None):
        super().__init__(client)

        if loop is None:
            loop = asyncio.get_event_loop()
        self._loop = loop

        if lock is None:
            lock = Lock(key, client=client, loop=loop)
        elif lock._loop is not self._loop:
            raise ValueError('loop argument must agree with lock')
        self._lock = lock

        self.key = normalize_key(key)
        if lock.key != self.key:
            raise ValueError('key argument must agree with lock')

        self.locked = lock.locked
        self.acquire = lock.acquire

    async def __aenter__(self):
        await self.acquire()
        return None

    async def __aexit__(self, exc_type, exc, tb):
        self.release()

    async def _watch(self):
        async for events in self.client.watch(self._cond_prefix,
                                              filters='noput'):
            for event in events:
                try:
                    key = event.kv.key.decode()
                    if key in self._waiters:
                        waiter = self._waiters.pop(key)
                        if not waiter.done():
                            waiter.set_result(True)
                    elif not self._waiters:
                        raise StopIteration
                except StopIteration:
                    pass
                    # return
                except Exception as e:
                    print('***', repr(e))

    async def wait(self):
        if not self.locked():
            raise RuntimeError('cannot wait on un-acquired lock')

        async with self._orderer:
            while True:
                cond_id = str(self._cond_id).zfill(19)
                cond_key = self._session_prefix + '/' + cond_id
                self._cond_id += 1

                cond = CreateRevision(cond_key) == 0,
                put = [request.Put(cond_key, '', self.session_id),
                       request.Delete(self._lock.owner)]  # release lock
                resp = await self.client.txn(cond, put, [])

                if resp.succeeded:
                    break
                # TODO find a good cond_id, based on newest key in session
                print('failed to find cond key')

        try:
            fut = self._loop.create_future()
            self._waiters[cond_key] = fut
            if self._watcher is None or self._watcher.done():
                self._watcher = self._loop.create_task(self._watch())

            await fut
        finally:
            cancelled = False
            while True:
                try:
                    await self.acquire()
                    break
                except asyncio.CancelledError:
                    cancelled = True

            if cancelled:
                raise asyncio.CancelledError

    async def wait_for(self, predicate):
        result = predicate()
        while not result:
            await self.wait()
            result = predicate()
        return result

    async def _notify_all(self):
        await self.client.delete_range(self._cond_prefix)

    def notify_all(self):
        self._loop.create_task(self._notify_all())

    def notify(self, n):
        raise NotImplementedError()

    def release(self):
        self._lock.release()

    @property
    def _cond_prefix(self):
        return self.key + '_condition/'

    @property
    def _session_prefix(self):
        return self._cond_prefix + str(self.client._session.id)

    @property
    def _orderer(self):
        return Condition._Common.orderers[self._session_prefix]

    @property
    def _watcher(self):
        return Condition._Common.watchers.get(self._session_prefix)

    @_watcher.setter
    def _watcher(self, value):
        Condition._Common.watchers[self._session_prefix] = value

    @property
    def _waiters(self):
        return Condition._Common.waiters[self._session_prefix]

    @property
    def _cond_id(self):
        return Condition._Common.cond_ids[self._session_prefix]

    @_cond_id.setter
    def _cond_id(self, value):
        Condition._Common.cond_ids[self._session_prefix] = value
