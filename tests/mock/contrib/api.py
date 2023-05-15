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

import abc
from unittest.mock import MagicMock

from requests import Request, Response

from bk_resource import APIResource


class MockAPIResource(APIResource, abc.ABC):
    base_url = "https://bk.tencent.com/"


class MockGetAPI(MockAPIResource):
    action = "/get_api/"
    method = "GET"


class MockPostAPI(MockAPIResource):
    action = "/post_api/"
    method = "POST"


class MockGetError(APIResource):
    base_url = "https://127.0.0.1:99999"
    action = "/"
    method = "GET"


class MockGetTypeError(MockGetError):
    def perform_request(self, validated_request_data):
        response = Response()
        response.status_code = 200
        response._content = []
        return self.parse_response(response)


class MockGetResultFalse(MockGetError):
    def perform_request(self, validated_request_data):
        response = Response()
        response.status_code = 200
        response._content = {"result": False, "code": 403}
        request = Request()
        request.url = self.base_url
        response.request = request
        return self.parse_response(response)


class MockSession(MagicMock):
    response = Response()
    response.status_code = 200
    response._content = {"result": True, "code": 0, "data": dict()}

    def get(self, *args, **kwargs):
        self.response._content = {"result": True, "code": 0, "data": {"headers": kwargs.get("headers", {})}}
        return self.response

    def request(self, *args, **kwargs):
        return self.response


class MockErrorSession(MockSession):
    response = Response()
    response.status_code = 403
    request = Request()
    request.url = "/"
    response.request = request
