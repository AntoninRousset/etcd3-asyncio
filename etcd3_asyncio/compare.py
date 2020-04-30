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


class CompareTarget(ABC):

    def __init__(self, target: str, key: str):
        self.target = target
        self.key = key

    def __eq__(self, other):
        return Compare('=', self.target, self.key, other)

    def __gt__(self, other):
        return Compare('>', self.target, self.key, other)

    def __lt__(self, other):
        return Compare('<', self.target, self.key, other)

    def __ne__(self, other):
        return Compare('!=', self.target, self.key, other)


class CreateRevision(CompareTarget):

    def __init__(self, key: str):
        super().__init__('create_revision', key)


class ModRevision(CompareTarget):

    def __init__(self, key: str):
        super().__init__('mod_revision', key)


class Value(CompareTarget):

    def __init__(self, key: str):
        super().__init__('value', key)


class Version(CompareTarget):

    def __init__(self, key: str):
        super().__init__('version', key)


class Compare:

    results = {'=': 0, '>': 1, '<': 2, '!=': 3}
    targets = {'version': 0, 'create_revision': 1, 'mod_revision': 2,
               'value': 3}

    def __init__(self, result: str, target: str, key: str, data: int):
        if result not in self.results:
            raise KeyError(f'Unknown compare result "{result}"')
        if target not in self.targets:
            raise KeyError(f'Unknown compare target "{target}"')

        if target == 'value':
            data = str(data).encode()
        else:
            data = int(data)

        self._compare = _etcd.Compare(result=self.results[result],
                                      target=self.targets[target],
                                      key=str(key).encode(), **{target: data})

