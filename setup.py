#!/usr/bin/env python

#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements. See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership. The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.
#


import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

# TODO generate python from .proto

setuptools.setup(
    name='etcd3-asyncio',
    version='0.1a1',
    license='Apache License 2.0',
    author='Antonin Rousset',
    description='Etcd v3 client using grpclib',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/AntoninRousset/etcd3-asyncio',
    packages=['etcd3_asyncio'],
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.6',
    install_requires=[
        'protobuf',
        'googleapis-common-protos',
    ],
)
