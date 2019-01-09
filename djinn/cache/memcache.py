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
import functools
import logging

import memcache
import six

from djinn.cache.base import AbstractCacheManager

logger = logging.getLogger(__name__)

def reconnect(func):
    @functools.wraps(func)
    def _wrapper(self, *args, **kwargs):
        try:
            ret = func(self, *args, **kwargs)
            return ret
        except Exception:
            logger.exception("memcache server closed!")
            self.close()
    return _wrapper


class MemcacheManager(AbstractCacheManager):

    def __init__(self, servers, timeout=3):
        self.servers = servers
        self.default_timeout = int(timeout)
        self._cache = memcache.Client(self.servers)

    @property
    def cache(self):
        if self._cache is None:
            self._cache = memcache.Client(self.servers)

        return self._cache

    @reconnect
    def add(self, key, value, timeout=0):
        if six.PY2 and isinstance(value, unicode):
            value = utf8(value)

        return self.cache.add(key, value,
                              timeout or self.default_timeout)

    @reconnect
    def get(self, key, default=None):
        val = self.cache.get(key)
        if val is None:
            return default

        if six.PY2 and isinstance(val, basestring):
            return utf8(val)

        return val

    @reconnect
    def set(self, key, value, timeout=0):
        if six.PY2 and isinstance(value, unicode):
            value = utf8(value)
        return self.cache.set(key, value,
                              timeout or self.default_timeout)

    @reconnect
    def delete(self, key):
        return self.cache.delete(key)

    @reconnect
    def get_many(self, keys):
        return self.cache.get_multi(keys)

    def close(self, **kwargs):
        try:
            self._cache.disconnect_all()
        except Exception:
            self._cache = None

    @reconnect
    def stats(self):
        return self.cache.get_stats()

    @reconnect
    def flush_all(self):
        self.cache.flush_all()
