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

from bk_resource import Resource
from tests.mock.models import User


class DirectResource(Resource):
    def perform_request(self, validated_request_data):
        return None


class NonCollectorResource(Resource):
    support_data_collect = False

    def perform_request(self, validated_request_data):
        return None


class ErrorResource(Resource):
    def perform_request(self, validated_request_data):
        raise TypeError()


class SerializerModuleRequestSerializer(serializers.Serializer):
    ...


class SerializerModuleResponseSerializer(serializers.Serializer):
    ...


class UserSerializer(serializers.ModelSerializer):
    resp_type = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = "__all__"


class UserResource(Resource):
    RequestSerializer = UserSerializer
    ResponseSerializer = UserSerializer

    def perform_request(self, validated_request_data):
        if validated_request_data.get("resp_type") == "model":
            return User(username=validated_request_data["username"])
        elif validated_request_data.get("resp_type") == "error":
            return {"username": User(username=validated_request_data["username"])}
        return validated_request_data


class RequestResource(Resource):
    def perform_request(self, validated_request_data):
        return validated_request_data["_request"]
