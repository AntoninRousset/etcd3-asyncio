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


def ensure_iter(obj, *, exceptions=[str]):
    for exception in exceptions:
        if isinstance(obj, exception):
            return (obj,)
    if hasattr(obj, '__iter__'):
        return obj
    else:
        return (obj,)


def range_end_for_prefix(prefix):
    return prefix[0:-1] + bytes([prefix[-1] + 1])
