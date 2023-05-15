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

from django.test import TestCase

from bk_resource.utils.local import (
    Local,
    local,
    with_client_operator,
    with_client_user,
    with_request_local,
)
from tests.constants.utils.local import DEFAULT_KEY, DEFAULT_USERNAME, DEFAULT_VALUE


class TestLocal(TestCase):
    def setUp(self):
        self.local = Local()

    def _set(self):
        setattr(self.local, DEFAULT_KEY, DEFAULT_VALUE)

    def _get(self):
        return getattr(self.local, DEFAULT_KEY)

    def _del(self):
        delattr(self.local, DEFAULT_KEY)

    def test_get_and_set(self):
        self._set()
        self.assertEqual(DEFAULT_VALUE, self._get())

    def test_get_error(self):
        key = "{}{}".format(DEFAULT_KEY, DEFAULT_KEY)
        with self.assertRaises(AttributeError):
            self.local.get(key)

    def test_set_and_del(self):
        self._set()
        self._del()

    def test_del_error(self):
        key = "{}{}".format(DEFAULT_KEY, DEFAULT_KEY)
        with self.assertRaises(AttributeError):
            delattr(self.local, key)

    def test_clear(self):
        self.local.clear()
        with self.assertRaises(AttributeError):
            self._get()


class TestWithRequestLocal(TestCase):
    def setUp(self) -> None:
        self.local = local
        self.local.username = DEFAULT_USERNAME

    def test(self):
        with with_request_local():
            with self.assertRaises(AttributeError):
                getattr(self.local, "username")
        self.assertEqual(DEFAULT_USERNAME, getattr(self.local, "username"))


class TestWithClientUser(TestCase):
    def setUp(self) -> None:
        self.local = local

    def test(self):
        username = "{}{}".format(DEFAULT_USERNAME, DEFAULT_USERNAME)
        with with_client_user(username):
            self.assertEqual(username, self.local.username)


class TestWithClientOperator(TestCase):
    def setUp(self) -> None:
        self.local = local

    def test(self):
        user = DEFAULT_USERNAME
        with with_client_operator(user):
            self.assertEqual(user, self.local.operator)
