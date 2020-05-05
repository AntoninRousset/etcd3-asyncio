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
from abc import ABC
from collections import defaultdict
from grpclib.client import Channel

from . import _etcd, request
from .utils import ensure_iter


class Client:

    def __init__(self, host='127.0.0.1', port=2379, *, ttl=10):
        self._channel = Channel(host, port)

        self._kvstub = _etcd.KVStub(self._channel)
        self._leasestub = _etcd.LeaseStub(self._channel)
        self._watchstub = _etcd.WatchStub(self._channel)

        self._session = self.Lease(ttl)

    def __del__(self):
        self._channel.close()

    def __await__(self):
        return self.start_session().__await__()

    async def start_session(self):
        await self._session.grant()
        return self

    def Condition(self, *args, **kwargs):
        from .condition import Condition
        return Condition(*args, **kwargs, client=self)

    def delete(self, *args, **kwargs):
        return request.Delete(*args, **kwargs, client=self).send()

    def delete_range(self, *args, **kwargs):
        return request.DeleteRange(*args, **kwargs, client=self).send()

    def get(self, *args, **kwargs) -> str:
        return request.Get(*args, **kwargs, client=self).send()

    def Lease(self, *args, **kwargs):
        from .lease import Lease
        return Lease(*args, **kwargs, client=self)

    def Lock(self, *args, **kwargs):
        from .lock import Lock
        return Lock(*args, **kwargs, client=self)

    def put(self, *args, **kwargs):
        return request.Put(*args, **kwargs, client=self).send()

    def range(self, *args, **kwargs):
        return request.Range(*args, **kwargs, client=self).send()

    def txn(self, compare, success, failure):
        compare = [c for c in ensure_iter(compare)]
        success = [RequestOp(s) for s in ensure_iter(success)]
        failure = [RequestOp(f) for f in ensure_iter(failure)]

        return request.Txn(compare, success, failure, client=self).send()

    def watch(self, *args, **kwargs):
        return request.Watch(*args, **kwargs, client=self).send()


class User:

    def __init__(self, client):
        self.client = client

    @property
    def session_id(self):
        return self.client._session.id


class RequestOp:

    def __init__(self, request: request.Request):
        self._request_op = _etcd.RequestOp(**{request.type: request._request})
