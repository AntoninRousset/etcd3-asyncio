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

from abc import ABC
from grpclib.client import Channel

from . import _etcd, request
from .request import Delete, Get, Put, Range, Txn
from .utils import ensure_iter


class Client:

    def __init__(self, host='127.0.0.1', port=2379):
        self._channel = Channel(host, port)
        self._kvstub = _etcd.KVStub(self._channel)

    def __del__(self):
        self._channel.close()

    def delete(self, key: str, range_end: str = ''):
        return request.Delete(key, range_end, client=self)

    def get(self, key: str) -> str:
        return request.Get(key, client=self)

    def put(self, key: str, value: str):
        return request.Put(key, value, client=self)

    def range(self, key: str, range_end: str = '', limit: int = 0) -> str:
        return request.Range(key, range_end, limit, client=self)

    def txn(self, compare, success, failure):
        compare = [c for c in ensure_iter(compare)]
        success = [RequestOp(s) for s in ensure_iter(success)]
        failure = [RequestOp(f) for f in ensure_iter(failure)]

        return request.Txn(compare, success, failure, client=self)


class RequestOp:

    def __init__(self, request: request.Request):
        self._request_op = _etcd.RequestOp(**{request.type: request._request})
