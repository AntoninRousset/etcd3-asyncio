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
from collections import OrderedDict

from .. import _etcd, get_client
from ..utils import ensure_iter, range_end_for_prefix


class Unary(ABC):

    def __init__(self, request, method, *, parse=True, client=None):
        self._request = request
        self._method = method
        self.parse = parse
        self._client = client

        self._response = None

    def __await__(self):
        return self.send().__await__()

    async def send(self):
        try:
            self._response = await self._method(self._request)
        except ConnectionRefusedError:
            raise RuntimeError('Could not connect to etcd')

        return self.result()

    def done(self):
        return self._response is not None

    def parse_response(self, response):
        return None

    def result(self):
        if not self.done():
            raise asyncio.InvalidStateError()
        if self.parse:
            return self.parse_response(self._response)
        return self._response

    def to_requestOp(self):
        raise TypeError(f'{self.__class__} cannot be cast in a RequestOp')


class DeleteRange(Unary):

    def __init__(self, key: str, range_end: str = None, *, client=None,
                 **kwargs):
        key = str(key).encode()
        if range_end is None:
            range_end = range_end_for_prefix(key)
        else:
            range_end = str(range_end).encode()
        if client is None:
            client = get_client()

        request = _etcd.DeleteRangeRequest(key=key, range_end=range_end)
        method = client._kvstub.DeleteRange
        super().__init__(request, method, client=client, **kwargs)

    def parse_response(self, response):
        return response.deleted

    def to_requestOp(self):
        return _etcd.RequestOp(request_delete_range=self._request)

    def read_responseOp(self, response: _etcd.ResponseOp):
        self._response = response.response_delete_range


class Delete(DeleteRange):

    def __init__(self, key: str, **kwargs):
        super().__init__(key, '', **kwargs)


class LeaseGrant(Unary):

    def __init__(self, TTL: int, ID: int = 0, *, client=None, **kwargs):
        if client is None:
            client = get_client()

        request = _etcd.LeaseGrantRequest(ID=int(ID), TTL=int(TTL))
        method = client._leasestub.LeaseGrant
        super().__init__(request, method, client=client, **kwargs)

    def parse_response(self, response):
        return response.ID


class LeaseRevoke(Unary):

    def __init__(self, ID: int, *, client=None, **kwargs):
        if client is None:
            client = get_client()

        request = _etcd.LeaseRevokeRequest(ID=int(ID))
        method = client._leasestub.LeaseRevokeRequest
        super().__init__(request, method, client=client, **kwargs)


class Put(Unary):

    def __init__(self, key: str, value: str, lease_id=0, *, client=None,
                 **kwargs):
        if client is None:
            client = get_client()

        request = _etcd.PutRequest(key=str(key).encode(),
                                   value=str(value).encode(), lease=lease_id)
        method = client._kvstub.Put
        super().__init__(request, method, client=client, **kwargs)

    def to_requestOp(self):
        return _etcd.RequestOp(request_put=self._request)

    def read_responseOp(self, response: _etcd.ResponseOp):
        self._response = response.response_put


class Range(Unary):

    _orders = {None: 0, 'ascend': 1, 'descend': 2}
    _targets = {'key': 0, 'version': 1, 'create': 2, 'mod': 3, 'value': 4}

    def __init__(self, key: str, range_end: str = None, limit: int = 0, *,
                 sort_order=None, sort_target='key', client=None, **kwargs):
        key = str(key).encode()
        if range_end is None:
            range_end = range_end_for_prefix(key)
        else:
            range_end = str(range_end).encode()
        if client is None:
            client = get_client()

        request = _etcd.RangeRequest(key=key, range_end=range_end, limit=limit,
                                     sort_order=Range._orders[sort_order],
                                     sort_target=Range._targets[sort_target])
        method = client._kvstub.Range
        super().__init__(request, method, client=client, **kwargs)

    def parse_response(self, response):
        res = [(kvs.key.decode(), kvs.value.decode()) for kvs in response.kvs]
        return OrderedDict(res)

    def to_requestOp(self) -> _etcd.RequestOp:
        return _etcd.RequestOp(request_range=self._request)

    def read_responseOp(self, response: _etcd.ResponseOp):
        self._response = response.response_range


class Get(Range):

    def __init__(self, key: str, default=None, **kwargs):
        super().__init__(key, '', 1, **kwargs)
        self.default = default

    def parse_response(self, response):
        if response.count >= 1:
            return response.kvs[0].value.decode()
        return self.default


class Txn(Unary):

    def __init__(self, compare=[], success=[], failure=[], *, client=None,
                 **kwargs):
        if client is None:
            client = get_client()

        self._s_requests = ensure_iter(success)
        self._f_requests = ensure_iter(failure)

        cs = [c._compare for c in ensure_iter(compare)]
        ss = [success.to_requestOp() for success in self._s_requests]
        fs = [failure.to_requestOp() for failure in self._f_requests]

        request = _etcd.TxnRequest(compare=cs, success=ss, failure=fs)
        method = client._kvstub.Txn
        super().__init__(request, method, client=client, **kwargs)

    def parse_response(self, response):
        requests = self._s_requests if response.succeeded else self._f_requests
        result = []
        for req, res in zip(requests, response.responses):
            req.read_responseOp(res)  # TODO, need to decode?
            result.append(req.result())
        return response.succeeded, result
