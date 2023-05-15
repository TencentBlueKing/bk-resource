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

from bk_resource.base import Resource
from bk_resource.contrib import APIResource, BkApiResource, CacheResource
from bk_resource.management.root import adapter, api, resource

default_app_config = "bk_resource.apps.BKResourceConfig"

__author__ = "蓝鲸智云"
__copyright__ = "Copyright (c)   2012-2021 Tencent BlueKing. All Rights Reserved."
__doc__ = """
自动发现项目下resource和adapter和api
    cc
    ├── adapter
    │   ├── default.py
    │   ├── community
    │   │   └── resources.py
    │   └── enterprise
    │       └── resources.py
    └── resources.py
    使用:
        resource.cc -> cc/resources.py
        # 调用resource.cc 即可访问对应文件下的resource
        adapter.cc -> cc/adapter/default.py -> cc/adapter/${platform}/resources.py
        # 调用adapter.cc 既可访问对应文件下的resource，
        # 如果在${platform}/resources.py里面有相同定义，会重载default.py下的resource
    """
__all__ = [
    "Resource",
    "CacheResource",
    "APIResource",
    "BkApiResource",
    "adapter",
    "api",
    "resource",
    "contrib",
]
