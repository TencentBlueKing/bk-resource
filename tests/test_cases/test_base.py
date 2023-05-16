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
from rest_framework import serializers

from bk_resource import Resource
from bk_resource.exceptions import ValidateException
from tests.mock import base
from tests.mock.base import (
    DirectResource,
    ErrorResource,
    NonCollectoResource,
    RequestResource,
    UserResource,
)
from tests.mock.models import User


class ResourceTest(TestCase):
    def test_call(self):
        result = DirectResource()()
        self.assertEqual(result, None)

    def test_none_support_data_collect(self):
        result = NonCollectoResource()()
        self.assertEqual(result, None)

    def test_request_exception(self):
        with self.assertRaises(TypeError):
            ErrorResource()()

    def test_get_data_string(self):
        _resource = DirectResource()
        # 测试正常转换
        data = _resource._get_data_string(dict())
        self.assertIsInstance(data, str)
        # 测试转换报错
        data = _resource._get_data_string({"object": object()})
        self.assertIsInstance(data, str)
        # 测试非常规类型转换
        data = _resource._get_data_string(object())
        self.assertIsInstance(data, str)

    def test_get_serializer(self):
        _resource = DirectResource()
        # 测试直接获取
        with self.assertRaises(AssertionError):
            serializer = _resource.request_serializer
            self.assertIsInstance(serializer, serializers.Serializer)
        with self.assertRaises(AssertionError):
            serializer = _resource.response_serializer
            self.assertIsInstance(serializer, serializers.Serializer)
        # 测试初始化后获取
        data = _resource.validate_request_data({})
        serializer = _resource.request_serializer
        self.assertEqual(data, {})
        self.assertEqual(serializer, None)
        data = _resource.validate_response_data({})
        serializer = _resource.response_serializer
        self.assertEqual(data, {})
        self.assertEqual(serializer, None)

    def test_serializer_module(self):
        class SerializerModuleResource(Resource):
            serializers_module = base

            def perform_request(self, validated_request_data):
                return None

        _resource = SerializerModuleResource()
        self.assertEqual(_resource.RequestSerializer.__class__, base.SerializerModuleRequestSerializer.__class__)
        self.assertEqual(_resource.ResponseSerializer.__class__, base.SerializerModuleResponseSerializer.__class__)

    def test_validate_request_data(self):
        _resource = UserResource()
        # 测试Model
        data = _resource(User(username="admin"))
        self.assertEqual(data, {"username": "admin"})
        # 测试JSON
        data = _resource({"username": "admin"})
        self.assertEqual(data, {"username": "admin"})
        # 测试JSON Invalid
        with self.assertRaises(ValidateException):
            _resource({})

    def test_validate_response_data(self):
        _resource = UserResource()
        # 测试Model
        data = _resource({"username": "admin", "resp_type": "model"})
        self.assertEqual(data, {"username": "admin"})
        # 测试Error
        with self.assertRaises(ValidateException):
            _resource({"username": "admin", "resp_type": "error"})

    def test_inject_request(self):
        _resource = RequestResource()
        _request = object()
        data = _resource(_request=_request)
        self.assertEqual(data, _request)

    def test_bulk_request(self):
        _resource = DirectResource()
        # 测试不可迭代对象
        with self.assertRaises(TypeError):
            _resource.bulk_request(object())
        # 测试正常请求
        data = _resource.bulk_request([{}])
        self.assertEqual(data, [None])
        # 测试错误请求
        _error_resource = ErrorResource()
        # 测试单个错误
        with self.assertRaises(TypeError):
            _error_resource.bulk_request([{}], ignore_exceptions=False)
        # 测试全部错误
        with self.assertRaises(TypeError):
            _error_resource.bulk_request([{}], ignore_exceptions=True)
