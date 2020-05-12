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
from abc import ABC, abstractmethod

from .. import _etcd, get_client
from ..utils import ensure_iter, range_end_for_prefix


class Stream(ABC):

    def __init__(self, request, method, resend, *, parse=True, client=None):
        self._request = request
        self._method = method
        self._resend = resend
        self.parse = parse
        self._client = client

    def __aiter__(self):
        return self.send()

    async def send(self):
        try:
            async with self._method.open() as stream:
                await stream.send_message(self._request)
                while True:
                    response = await stream.recv_message()
                    if self.parse:
                        yield self.parse_response(response)
                    else:
                        yield response
                    if self._resend:
                        await stream.send_message(self._request)
        except ConnectionRefusedError:
            raise RuntimeError('Could not connect to etcd')

    def parse_response(self, response):
        return None


class LeaseKeepAlive(Stream):

    def __init__(self, ID: int, *, client=None, **kwargs):
        if client is None:
            client = get_client()

        request = _etcd.LeaseKeepAliveRequest(ID=int(ID))
        method = client._leasestub.LeaseKeepAlive
        super().__init__(request, method, True, client=client, **kwargs)

    def parse_response(self, response):
        return response.TTL


class Watch(Stream):

    filter_types = {'noput': 0, 'nodelete': 1}

    def __init__(self, key: str, range_end: str = None, *, start_revision=None,
                 filters: str = [], client=None, **kwargs):
        key = str(key).encode()
        if client is None:
            client = get_client()
        if range_end is None:
            range_end = range_end_for_prefix(key)
        else:
            range_end = str(range_end).encode()

        filters = [self.filter_types[f] for f in ensure_iter(filters)]

        request = _etcd.WatchRequest(
            create_request=_etcd.WatchCreateRequest(
                    key=key,
                    range_end=range_end,
                    start_revision=start_revision,
                    filters=filters
                )
            )
        method = client._watchstub.Watch
        super().__init__(request, method, False, client=client, **kwargs)

    def parse_response(self, response):
        return response.events  # TODO
