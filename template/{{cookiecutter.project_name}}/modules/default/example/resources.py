# -*- coding: utf-8 -*-

import abc

from bk_resource import Resource, api
from blueapps.utils.request_provider import get_request_username

from modules.default.example.serializers import (
    UserInfoRequestSerializer,
    UserInfoResponseSerializer,
)


class ExampleBaseResource(Resource, abc.ABC):
    tags = ["Example"]


class UserInfoResource(ExampleBaseResource):
    name = "示例"
    RequestSerializer = UserInfoRequestSerializer
    ResponseSerializer = UserInfoResponseSerializer

    def perform_request(self, validated_request_data):
        username = get_request_username()
        return {
            "user_info": api.user_manage.retrieve_user(id=username),
            "request_username": username,
        }
