# -*- coding: utf-8 -*-
"""
TencentBlueKing is pleased to support the open source community by making
蓝鲸智云 - Resource SDK (BlueKing - Resource SDK) available.
Copyright (C) 2023 THL A29 Limited,
a Tencent company. All rights reserved.
Licensed under the MIT License (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at https://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
either express or implied. See the License for the
specific language governing permissions and limitations under the License.
We undertake not to change the open source license (MIT license) applicable
to the current version of the project delivered to anyone in the future.
"""

import random
import time

from django.test import TestCase

from bk_resource.utils.cache import CacheTypeItem, InstanceCache, using_cache
from tests.constants.utils.cache import (
    DEFAULT_CACHE_DATA,
    DEFAULT_CACHE_KEY,
    DEFAULT_CACHE_TIMEOUT,
)


class TestUsingCache(TestCase):
    def setUp(self) -> None:
        cache_type = CacheTypeItem(DEFAULT_CACHE_KEY, DEFAULT_CACHE_TIMEOUT)
        self.cache_type = cache_type
        self.cache = using_cache(cache_type=cache_type)

    def _get(self):
        return self.cache.get_value(DEFAULT_CACHE_KEY)

    def _set(self):
        self.cache.set_value(DEFAULT_CACHE_KEY, DEFAULT_CACHE_DATA, DEFAULT_CACHE_TIMEOUT)

    def test_set_and_get(self):
        self._set()
        self.assertEqual(DEFAULT_CACHE_DATA, self._get())

    def test_wrapper_cache(self):
        @self.cache
        def cached_func():
            return random.random()

        x = cached_func()
        y = cached_func()
        self.assertEqual(x, y)

        time.sleep(DEFAULT_CACHE_TIMEOUT)
        z = cached_func()
        self.assertNotEqual(x, z)


class TestInstanceCache(TestCase):
    def setUp(self) -> None:
        self.instance = InstanceCache.instance()

    def _set(self):
        self.instance.set(DEFAULT_CACHE_KEY, DEFAULT_CACHE_DATA, DEFAULT_CACHE_TIMEOUT)

    def _clear(self):
        self.instance.clear()

    def _get(self):
        return self.instance.get(DEFAULT_CACHE_KEY)

    def _exists(self):
        return self.instance.exists(DEFAULT_CACHE_KEY)

    def _delete(self):
        self.instance.delete(DEFAULT_CACHE_KEY)

    def test_set_and_get(self):
        self._set()
        self.assertEqual(DEFAULT_CACHE_DATA, self._get())

    def test_exists(self):
        self._set()
        self.assertTrue(self._exists())

    def test_delete(self):
        self._delete()
        self.assertFalse(self._exists())

    def test_clear(self):
        self._clear()
        self.assertFalse(self._exists())
