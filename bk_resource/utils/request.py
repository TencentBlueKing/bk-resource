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
from typing import Optional, Type

from django.http import HttpRequest
from django.test import RequestFactory
from django.urls import Resolver404, resolve

from bk_resource.utils.local import local


def get_request_username(default=""):
    try:
        from blueapps.utils.request_provider import get_local_request

        username = get_local_request().user.username
    except Exception:  # pylint: disable=broad-except
        username = get_local_username()
        if not username:
            username = default
    return username


def get_local_username():
    """从local对象中获取用户信息（celery）"""
    return getattr(local, "username", None)


def set_local_username(username):
    local.username = username


def get_mock_request(**kwargs):
    return RequestFactory().request(**kwargs)


def get_resource_by_request(request: HttpRequest = None) -> Optional[Type["bk_resource.Resource"]]:
    """根据 request 对象获取具体的 Resource 类"""

    from blueapps.utils.request_provider import get_local_request

    request = request or get_local_request()
    if not request:
        return None

    try:
        match = resolve(request.path_info)
    except Resolver404:
        try:
            match = resolve(f"{request.path_info}/")
        except Resolver404:
            return None

    try:
        from bk_resource.viewsets import RESOURCE_MAPPING

        view_set_path = f"{match.func.cls.__module__}.{match.func.cls.__name__}"
        resource_clz = RESOURCE_MAPPING.get(
            (request.method, f"{view_set_path}.{match.func.actions.get(request.method.lower())}")
        )
        return resource_clz
    except Exception:  # pylint: disable=broad-except
        return None
