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
from unittest import mock

from django.core.handlers.wsgi import WSGIRequest
from django.test import TestCase

from bk_resource.utils.local import local
from bk_resource.utils.request import (
    get_mock_request,
    get_request_username,
    set_local_username,
)
from tests.constants.utils.request import DEFAULT_USERNAME
from tests.mock.utils.request import GetLocalRequest


class TestGetRequestUsername(TestCase):
    def test(self):
        self.assertIsNotNone(get_request_username())

    @mock.patch("blueapps.utils.request_provider.get_local_request", GetLocalRequest)
    def test_error(self):
        self.assertIsNotNone(get_request_username())

    @mock.patch("blueapps.utils.request_provider.get_local_request", GetLocalRequest)
    def test_default(self):
        local.username = None
        self.assertEqual(DEFAULT_USERNAME, get_request_username(DEFAULT_USERNAME))


class TestSetLocalUsername(TestCase):
    def test(self):
        username = random.random()
        set_local_username(username)
        self.assertEqual(username, local.username)


class TestMockRequest(TestCase):
    def test(self):
        self.assertIsInstance(get_mock_request(), WSGIRequest)
