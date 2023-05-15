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
import json

import requests
from django.conf import settings

from bk_resource.contrib.api import APIResource
from bk_resource.exceptions import IAMNoPermission, PlatformAuthParamsNotExist
from bk_resource.settings import bk_resource_settings
from bk_resource.utils.common_utils import is_backend


class BkApiResource(APIResource, abc.ABC):
    method = "GET"
    bkapi_header_authorization = False
    platform_authorization = False

    def add_platform_auth_params(self, params, force_platform_auth=False):
        """
        在以下情况不使用
        1. 未开启了平台鉴权
        2. API 未启用平台鉴权且不是后台任务
        """
        enable_platform_auth = bk_resource_settings.PLATFORM_AUTH_ENABLED
        if not enable_platform_auth or (not self.platform_authorization and not force_platform_auth):
            return params
        # 更新平台鉴权信息
        for _key in self.oath_cookies_params.keys():
            params.pop(_key, None)
        auth_token = bk_resource_settings.PLATFORM_AUTH_ACCESS_TOKEN
        auth_username = bk_resource_settings.PLATFORM_AUTH_ACCESS_USERNAME
        if not auth_token and not auth_username:
            raise PlatformAuthParamsNotExist()
        if auth_token:
            params["access_token"] = auth_token
        if auth_username:
            params["bk_username"] = auth_username
        return params

    def add_esb_info_before_request(self, params):
        """
        通过 params 参数控制是否检查 request
        @param {Boolean} [params.no_request] 是否需要带上 request 标识
        """
        params["bk_app_code"] = settings.APP_CODE
        params["bk_app_secret"] = settings.SECRET_KEY

        # 后台程序或非request请求直接返回
        if is_backend() or params.get("_is_backend", False):
            params.pop("_request", None)
            params = self.add_platform_auth_params(params, force_platform_auth=True)
            return params

        # 前端应用, _request，用于并发请求的场景
        from blueapps.utils.request_provider import get_local_request

        _request = params.get("_request")
        req = _request or get_local_request()
        auth_info = self.build_auth_args(req)
        params.update(auth_info)
        params["bk_username"] = getattr(req.user, "bk_username", None) or req.user.username
        params.pop("_request", None)

        # 平台鉴权兼容
        params = self.add_platform_auth_params(params)

        return params

    def build_auth_args(self, request):
        """组装认证信息"""
        auth_args = {}
        if request is None:
            return auth_args

        for key, value in self.oath_cookies_params.items():
            if value in request.COOKIES:
                auth_args.update({key: request.COOKIES[value]})
        return auth_args

    @property
    def oath_cookies_params(self):
        return getattr(settings, "OAUTH_COOKIES_PARAMS", {"bk_token": "bk_token"})

    def build_request_data(self, validated_request_data):
        return self.add_esb_info_before_request(validated_request_data)

    def build_header(self, validated_request_data):
        # 初始化
        headers = {}
        # 透传 Cookie
        from blueapps.utils.request_provider import get_local_request

        request = get_local_request()
        if request is not None:
            headers["cookie"] = "; ".join(
                [
                    f"{key}={val}"
                    for key, val in request.COOKIES.items()
                    if key in bk_resource_settings.REQUEST_BKAPI_COOKIE_FIELDS
                ]
            )
        # 鉴权参数
        if not self.bkapi_header_authorization:
            return headers
        return {
            **headers,
            "x-bkapi-authorization": json.dumps(
                self.add_platform_auth_params(
                    {
                        "bk_app_code": settings.APP_CODE,
                        "bk_app_secret": settings.SECRET_KEY,
                    }
                )
            ),
        }

    def parse_response(self, response: requests.Response):
        """
        兼容IAM无权限处理
        """

        try:
            result_json = response.json()
        except Exception:
            result_json = []

        if isinstance(result_json, dict) and str(result_json.get("code")) == IAMNoPermission().code:
            data = result_json.get("data", {})
            if result_json.get("permission"):
                data["permission"] = result_json["permission"]
            raise IAMNoPermission(data=json.dumps(data))

        return super().parse_response(response)
