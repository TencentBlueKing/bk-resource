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

from unittest import mock

from django.test import TestCase, override_settings

from bk_resource.exceptions import PlatformAuthParamsNotExist
from tests.mock.contrib.api import MockSession
from tests.mock.contrib.bk_api import (
    MockApiResource,
    MockHeaderInject,
    MockPlatformAuth,
    MockRequest,
)


class TestBkApiResource(TestCase):
    @mock.patch("bk_resource.contrib.api.requests.session", MockSession)
    def test_success(self):
        MockApiResource().request()

    @mock.patch("bk_resource.contrib.api.requests.session", MockSession)
    @mock.patch("bk_resource.contrib.bk_api.is_backend", mock.Mock(return_value=False))
    def test_success_not_backend(self):
        MockApiResource().request(_request=MockRequest())

    @mock.patch("bk_resource.contrib.api.requests.session", MockSession)
    def test_header_auth(self):
        MockHeaderInject().request()

    @override_settings(
        BK_RESOURCE={
            "PLATFORM_AUTH_ENABLED": True,
            "PLATFORM_AUTH_ACCESS_TOKEN": "admin",
            "PLATFORM_AUTH_ACCESS_USERNAME": "admin",
        }
    )
    @mock.patch("bk_resource.contrib.api.requests.session", MockSession)
    def test_platform_auth(self):
        MockPlatformAuth().request()

    @override_settings(BK_RESOURCE={"PLATFORM_AUTH_ENABLED": True})
    @mock.patch("bk_resource.contrib.api.requests.session", MockSession)
    def test_platform_auth_error(self):
        with self.assertRaises(PlatformAuthParamsNotExist):
            MockPlatformAuth().request()

    @override_settings(
        BK_RESOURCE={
            "REQUEST_BKAPI_COOKIE_FIELDS": ["username"],
        }
    )
    @mock.patch("bk_resource.contrib.bk_api.get_local_request", MockRequest)
    @mock.patch("bk_resource.contrib.api.requests.session", MockSession)
    def test_custom_cookie_fields(self):
        resp = MockApiResource().request()
        self.assertEqual(resp, {"headers": {"cookie": "username=admin"}})
