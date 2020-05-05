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

from . import client, request


class Lease(client.User):

    def __init__(self, ttl, id=0, *, client, loop=None):
        super().__init__(client)

        if loop is None:
            loop = asyncio.get_event_loop()
        self._loop = loop

        self.ttl = ttl
        self.id = id

        self._keeping_alive = None

    def __await__(self):
        return self.grant().__await__()

    async def __keep_alive(self):
        keepalive = request.LeaseKeepAlive(self.id, client=self.client)
        try:
            async for ttl in keepalive.send():
                await asyncio.sleep(ttl/3)
        except Exception as e:
            print(repr(e))

    async def grant(self, *, keepalive=True):
        self.id = await request.LeaseGrant(self.ttl, self.id,
                                           client=self.client).send()
        if keepalive:
            self._keepingalive = self._loop.create_task(self.__keep_alive())
        return self.id

    async def revoke(self):
        self._keeping_alive.cancel()
        await request.LeaseRevoke(self.id, client=self.client).send()
