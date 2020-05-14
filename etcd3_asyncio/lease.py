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

from . import request
from .client import get_client


class Lease():

    def __init__(self, ttl, id=0, *, client=None, loop=None):
        if client is None:
            client = get_client
        if loop is None:
            loop = asyncio.get_event_loop()

        self.ttl = ttl
        self.id = id
        self._client = client
        self._loop = loop

        self._granted = False
        self._granting = asyncio.Lock()
        self._heart = None

    def __await__(self):
        return self.grant().__await__()

    async def __keep_alive(self):
        keepalive = request.LeaseKeepAlive(self.id, client=self._client)
        try:
            async for ttl in keepalive:
                await asyncio.sleep(ttl/3)
        finally:
            self._granted = False

    async def grant(self, *, keepalive=True):
        async with self._granting:
            if self._granted:
                return
            self.id = await request.LeaseGrant(self.ttl, self.id,
                                               client=self._client)
            if keepalive:
                self._heart = self._loop.create_task(self.__keep_alive())
            self._granted = True
            return self.id

    async def revoke(self):
        self._heart.cancel()
        await request.LeaseRevoke(self.id, client=self._client)
