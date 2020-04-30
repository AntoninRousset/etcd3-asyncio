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

from abc import ABC, abstractmethod

from . import _etcd
from .utils import ensure_iter


class Request(ABC):

    def __init__(self, client, type: str, request):
        self.client = client
        self.type = type
        self._request = request

    def __await__(self):
        return self.send().__await__()

    async def send(self):
        if self.client is None:
            raise RuntimeError('Request needs a client')
        try:
            return self.parse_response(await self._method(self._request))
        except ConnectionRefusedError:
            raise RuntimeError('Could not connect to etcd')

    @property
    @abstractmethod
    def _method(self):
        pass

    @abstractmethod
    def parse_response(self, response):
        pass


class Delete(Request):

    def __init__(self, key: str, range_end: str, client=None):
        super().__init__(
            client, 'request_delete_range',
            _etcd.DeleteRangeRequest(key, range_end)
        )

    def parse_response(self, response):
        return None

    @property
    def _method(self):
        return self.client._kvstub.DeleteRange


class Put(Request):

    def __init__(self, key: str, value: str, client=None):
        super().__init__(
            client, 'request_put',
            _etcd.PutRequest(key=str(key).encode(), value=str(value).encode())
        )

    def parse_response(self, response):
        return None

    @property
    def _method(self):
        return self.client._kvstub.Put


class Range(Request):

    def __init__(self, key: str, range_end: str, limit: int, client=None):
        super().__init__(
            client, 'request_range',
            _etcd.RangeRequest(key=str(key).encode(),
                               range_end=str(range_end).encode(), limit=limit)
            )

    def parse_response(self, response):
        for kvs in response.kvs:
            yield kvs.key.decode(), kvs.value.decode()

    @property
    def _method(self):
        return self.client._kvstub.Range


class Txn(Request):

    def __init__(self, compare, success, failure, client=None):
        compare = [c._compare for c in ensure_iter(compare)]
        success = [s._request_op for s in ensure_iter(success)]
        failure = [f._request_op for f in ensure_iter(failure)]

        super().__init__(
            client, 'request_txn',
            _etcd.TxnRequest(compare=compare, success=success, failure=failure)
            )

    def parse_response(self, response):
        return response.succeeded

    @property
    def _method(self):
        return self.client._kvstub.Txn


class Get(Range):

    def __init__(self, key: str, client=None):
        super().__init__(key, '', 1, client=client)

    def parse_response(self, response):
        if response.count >= 1:
            return response.kvs[0].value.decode()

