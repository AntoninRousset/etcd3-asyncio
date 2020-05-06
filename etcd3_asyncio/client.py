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

from grpclib.client import Channel

from . import _etcd


class Client:

    def __init__(self, host='127.0.0.1', port=2379, *, ttl=10):
        self._channel = Channel(host, port)

        self._kvstub = _etcd.KVStub(self._channel)
        self._leasestub = _etcd.LeaseStub(self._channel)
        self._watchstub = _etcd.WatchStub(self._channel)

        from .lease import Lease
        self._session = Lease(ttl, client=self)

    def __del__(self):
        self._channel.close()

    async def start_session(self):
        await self._session.grant()

    @property
    def session_id(self):
        return self._session.id


_running_client = None


def get_client():
    global _running_client
    if _running_client is None:
        _running_client = Client()
    return _running_client
