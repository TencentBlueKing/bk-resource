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

from bk_resource import resource
from bk_resource.viewsets import ResourceRoute, ResourceViewSet

from .resources import UpdateUserInfoResource


# 声明 ViewSet，其中，ViewSet前方的内容会成为 url 的一部分
class UserInfoViewSet(ResourceViewSet):
    # 声明所有方法
    # Resource 会自动查找所有的子类并添加到 resource 中
    # 映射关系为 underscore_to_camel; 即 UpdateUserInfo => update_user_info
    resource_routes = [
        # 在这一条路由中，app0 为 APP 名，update_user_info 为 app0 下 resources.py 文件中的 UpdateUserInfoResource 对象
        # endpoint 不填写时默认为空，映射为根路由
        ResourceRoute("POST", resource.app0.update_user_info, endpoint="info"),
        # 我们也可以使用常规的方式进行声明，但不推荐
        ResourceRoute("POST", UpdateUserInfoResource),
        # 如果我们涉及到了 RestFul 标准的更新、删除类型，则可以使用 pk_field 声明，会自动将 pk 添加到 validated_request_data 中
        ResourceRoute("PUT", UpdateUserInfoResource, pk_field="user_id"),
    ]
