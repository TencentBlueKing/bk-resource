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

from blueapps.utils.request_provider import get_local_request

from bk_resource import Resource

from .serializers import (
    UpdateUserInfoRequestSerializer,
    UpdateUserInfoResponseSerializer,
)


class UpdateUserInfoResource(Resource):
    """更新用户信息"""

    # 声明输入输出使用的 Serializer
    # 声明 RequestSerializer 后，所有请求都会自动校验，validated_request_data 可以直接获取校验完成的数据
    RequestSerializer = UpdateUserInfoRequestSerializer
    # 声明 ResponseSerializer 后，所有输出会自动校验
    ResponseSerializer = UpdateUserInfoResponseSerializer

    def perform_request(self, validated_request_data):
        # 获取 Request 对象
        request = get_local_request()
        # 获取 User 对象
        user = request.user
        # 获取新用户名并更新
        new_username = validated_request_data["new_username"]
        user.username = new_username
        user.save()
        # 可以直接返回 User 对象，会按照 Serializer 自动格式化为对应的内容，当然，直接返回对应的字典格式也是可以的
        return user
