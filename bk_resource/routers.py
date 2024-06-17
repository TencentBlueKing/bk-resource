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

from rest_framework.routers import DefaultRouter
from rest_framework.viewsets import GenericViewSet

from bk_resource.tools import get_underscore_viewset_name
from bk_resource.viewsets import ResourceViewSet


class ResourceRouter(DefaultRouter):
    @staticmethod
    def _init_resource_viewset(viewset):
        """
        初始化ResourceViewset，动态增加方法，在register router前必须进行调用
        @:param viewset: ResourceViewset类
        """
        if isinstance(viewset, type) and issubclass(viewset, ResourceViewSet):
            viewset.generate_endpoint()

    def register(self, prefix, viewset, base_name=None):
        """
        注册单个ResourceViewset
        """
        self._init_resource_viewset(viewset)
        super(ResourceRouter, self).register(prefix, viewset, base_name)

    def register_module(self, viewset_module, prefix=None):
        """
        注册整个ResourceViewset模块，并根据类的命名规则自动生成对应的url
        """
        for attr, viewset in viewset_module.__dict__.items():
            # 全小写的属性不是类，忽略
            if attr.startswith("_") or attr[0].islower():
                continue
            # viewset is not ResourceViewSet：
            # 1. 在 DRF >= 3.15.0 版本，重复注册会抛出 ImproperlyConfigured 异常
            # 2. 对于用户导入的 ResourceViewSet 类不需要注册
            if isinstance(viewset, type) and issubclass(viewset, GenericViewSet) and viewset is not ResourceViewSet:
                module_prefix = self.get_default_basename(viewset)
                if prefix:
                    module_prefix = f"{prefix}/{module_prefix}" if module_prefix else prefix
                self.register(module_prefix, viewset)

    def get_default_basename(self, viewset):
        return get_underscore_viewset_name(viewset)
