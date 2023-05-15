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

from rest_framework import serializers


class ErrorResponseSerializer(serializers.Serializer):
    result = serializers.BooleanField()
    code = serializers.IntegerField()
    message = serializers.CharField()
    data = serializers.JSONField()


class ResponseBuilder:
    serializer = None

    def __init__(self, *, resource_class=None, data_serializer=None, name=None, **kwargs):
        self.serializer = self.build_serializer(
            resource_class=resource_class, data_serializer=data_serializer, name=name, **kwargs
        )

    def build_serializer(self, *, resource_class=None, data_serializer=None, name=None, **kwargs):
        raise NotImplementedError


class PaginatorResponseBuilder(ResponseBuilder):
    def build_serializer(self, *, resource_class=None, data_serializer=None, name=None, **kwargs):
        class PaginatorSerializer(serializers.Serializer):
            page = serializers.IntegerField()
            num_pages = serializers.IntegerField()
            total = serializers.IntegerField()
            results = data_serializer

            class Meta:
                ref_name = "[{}]".format(name or resource_class.__name__)

        return PaginatorSerializer()


class StandardResponseBuilder(ResponseBuilder):
    def build_serializer(self, *, resource_class=None, data_serializer=None, name=None, **kwargs):
        class ResponseSerializer(serializers.Serializer):
            result = serializers.BooleanField()
            code = serializers.IntegerField()
            message = serializers.CharField()
            request_id = serializers.CharField()
            data = data_serializer

            class Meta:
                ref_name = name or "{}.{}".format(resource_class.__module__, resource_class.__name__)

        return ResponseSerializer()
