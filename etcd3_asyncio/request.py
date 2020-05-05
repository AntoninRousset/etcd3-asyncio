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

    def __init__(self, client, type: str, parse, request):
        self.client = client
        self.type = type
        self.parse = parse
        self._request = request

    @abstractmethod
    async def send(self):
        pass

    @property
    @abstractmethod
    def _method(self):
        pass

    def parse_response(self, response):
        return None


class Unary(Request):

    async def send(self):
        if self.client is None:
            raise RuntimeError('Request needs a client')

        try:
            response = await self._method(self._request)
        except ConnectionRefusedError:
            raise RuntimeError('Could not connect to etcd')

        if self.parse:
            return self.parse_response(response)
        return response


class Stream(Request):

    def __init__(self, client, type: str, parse, request, resend):
        super().__init__(client, type, parse, request)

        self.resend = resend

    async def send(self):
        if self.client is None:
            raise RuntimeError('Request needs a client')

        try:
            async with self._method.open() as stream:
                await stream.send_message(self._request)
                while True:
                    response = await stream.recv_message()
                    if self.parse:
                        yield self.parse_response(response)
                    else:
                        yield response
                    if self.resend:
                        await stream.send_message(self._request)
        except ConnectionRefusedError:
            raise RuntimeError('Could not connect to etcd')


class DeleteRange(Unary):

    def __init__(self, key: str, range_end: str = None, *, parse=True,
                 client=None):
        if range_end is None:
            range_end = str(key).encode()
            range_end = range_end[0:-1] + bytes([range_end[-1] + 1])
        else:
            range_end = str(range_end).encode()

        super().__init__(
            client, 'request_delete_range', parse,
            _etcd.DeleteRangeRequest(key=str(key).encode(),
                                     range_end=range_end)
        )

    @property
    def _method(self):
        return self.client._kvstub.DeleteRange


class LeaseGrant(Unary):

    def __init__(self, TTL: int, ID: int = 0, *, parse=True, client=None):
        super().__init__(
            client, 'request_lease_grant', parse,
            _etcd.LeaseGrantRequest(ID=int(ID), TTL=int(TTL))
        )

    def parse_response(self, response):
        return response.ID

    @property
    def _method(self):
        return self.client._leasestub.LeaseGrant


class LeaseRevoke(Unary):

    def __init__(self, ID: int, *, parse=True, client=None):
        super().__init__(
            client, 'request_lease_revoke', parse,
            _etcd.LeaseRevokeRequest(ID=int(ID))
        )

    @property
    def _method(self):
        return self.client._leasestub.LeaseRevoke


class LeaseKeepAlive(Stream):

    def __init__(self, ID: int, *, parse=True, client=None):
        super().__init__(
            client, 'request_lease_keepalive', parse,
            _etcd.LeaseKeepAliveRequest(ID=int(ID)), resend=True
        )

    def parse_response(self, response):
        return response.TTL

    @property
    def _method(self):
        return self.client._leasestub.LeaseKeepAlive


class Put(Unary):

    def __init__(self, key: str, value: str, lease_id=0, *, parse=True,
                 client=None):
        super().__init__(
            client, 'request_put', parse,
            _etcd.PutRequest(key=str(key).encode(), value=str(value).encode(),
                             lease=lease_id)
        )

    @property
    def _method(self):
        return self.client._kvstub.Put


class Range(Unary):

    sort_orders = {None: 0, 'ascend': 1, 'descend': 2}
    sort_targets = {'key': 0, 'version': 1, 'create': 2, 'mod': 3, 'value': 4}

    def __init__(self, key: str, range_end: str = None, limit: int = 0, *,
                 sort_order=None, sort_target='key', parse=True, client=None):

        if range_end is None:
            range_end = str(key).encode()
            range_end = range_end[0:-1] + bytes([range_end[-1] + 1])
        else:
            range_end = str(range_end).encode()

        super().__init__(
            client, 'request_range', parse,
            _etcd.RangeRequest(key=str(key).encode(),
                               range_end=range_end, limit=limit,
                               sort_order=self.sort_orders[sort_order],
                               sort_target=self.sort_targets[sort_target])
            )

    def parse_response(self, response):
        for kvs in response.kvs:
            yield kvs.key.decode(), kvs.value.decode()

    @property
    def _method(self):
        return self.client._kvstub.Range


class Txn(Unary):

    def __init__(self, compare, success, failure, *, parse=False, client=None):
        compare = [c._compare for c in ensure_iter(compare)]
        success = [s._request_op for s in ensure_iter(success)]
        failure = [f._request_op for f in ensure_iter(failure)]

        super().__init__(
            client, 'request_txn', parse,
            _etcd.TxnRequest(compare=compare, success=success, failure=failure)
            )

    def parse_response(self, response):
        return response.succeeded

    @property
    def _method(self):
        return self.client._kvstub.Txn


class Watch(Stream):

    filter_types = {'noput': 0, 'nodelete': 1}

    def __init__(self, key: str, range_end: str = None, *, start_revision=None,
                 filters: str = [], parse=True, client=None):
        filters = [self.filter_types[f] for f in ensure_iter(filters)]

        if range_end is None:
            range_end = str(key).encode()
            range_end = range_end[0:-1] + bytes([range_end[-1] + 1])
        else:
            range_end = str(range_end).encode()

        super().__init__(
            client, 'request_watch_create', parse,
            _etcd.WatchRequest(
                create_request=_etcd.WatchCreateRequest(
                    key=str(key).encode(),
                    range_end=range_end,
                    start_revision=start_revision,
                    filters=filters
                )
            ), resend=False
        )

    def parse_response(self, response):
        return response.events

    @property
    def _method(self):
        return self.client._watchstub.Watch


class Delete(DeleteRange):

    def __init__(self, key: str, *, parse=True, client=None):
        super().__init__(key, '', parse=parse, client=client)


class Get(Range):

    def __init__(self, key: str, default=None, *, parse=True, client=None):
        super().__init__(key, '', 1, parse=parse, client=client)
        self.default = default

    def parse_response(self, response):
        if response.count >= 1:
            return response.kvs[0].value.decode()
        return self.default
