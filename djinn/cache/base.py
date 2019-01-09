# -*- coding: utf-8 -*-
#
# Copyright(c) 2014 palmhold.com
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import abc

import six

@six.add_metaclass(abc.ABCMeta)
class AbstractCacheManager(object):

    @abc.abstractmethod
    def get(self, key, default=None):
        pass
    
    @abc.abstractmethod
    def add(self, key, value, timeout=0):
        pass

    @abc.abstractmethod
    def set(self, key, value, timeout=0):
        pass

    @abc.abstractmethod
    def delete(self, key):
        pass

    @abc.abstractmethod
    def get_many(self, keys):
        pass

    @abc.abstractmethod
    def flush_all(self):
        pass

    @abc.abstractmethod
    def close(self):
        pass
