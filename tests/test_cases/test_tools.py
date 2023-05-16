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
from rest_framework.fields import empty

from bk_resource.tools import (
    format_serializer_errors,
    get_serializer_fields,
    get_underscore_viewset_name,
    render_schema,
)
from tests.constants.tools import (
    DEFAULT_RENDER_LIST,
    DEFAULT_SCHEMA_RESULT,
    SERIALIZER_ERROR_MESSAGE,
    UserInfoSerializer,
)


class TestGetSerializerFields(TestCase):
    def test_non_serializer(self):
        self.assertEqual([], get_serializer_fields(None))

    def test_not_serializer(self):
        self.assertEqual([], get_serializer_fields(object))

    def test_serializer(self):
        fields = get_serializer_fields(UserInfoSerializer)
        for field in fields:
            self.assertEqual(empty, field["default"])
            field.pop("default", None)
            if "items" in field.keys():
                field["items"].pop("default", None)
        self.assertEqual(DEFAULT_SCHEMA_RESULT, fields)


class TestRenderSchema(TestCase):
    def test(self):
        fields = get_serializer_fields(UserInfoSerializer)
        value = render_schema(fields)
        self.assertEqual(DEFAULT_RENDER_LIST, value)


class TestGetUnderscoreViewSetName(TestCase):
    def test(self):
        class ABCViewSet:
            ...

        self.assertEqual("abc", get_underscore_viewset_name(ABCViewSet))


class TestFormatSerializerErrors(TestCase):
    def test(self):
        serializer = UserInfoSerializer(data={})
        serializer.is_valid()
        self.assertEqual(SERIALIZER_ERROR_MESSAGE, format_serializer_errors(serializer))

    def test_error(self):
        serializer = UserInfoSerializer()
        with self.assertRaises(AssertionError):
            format_serializer_errors(serializer)
