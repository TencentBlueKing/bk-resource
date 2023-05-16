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

from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator


class BKResourceOpenAPISchemaGenerator(OpenAPISchemaGenerator):
    def get_path_item(self, path, view_cls, operations):
        """Get a :class:`.PathItem` object that describes the parameters and operations related to a single path in the
        API.

        :param str path: the path
        :param type view_cls: the view that was bound to this path in urlpatterns
        :param dict[str,openapi.Operation] operations: operations defined on this path, keyed by lowercase HTTP method
        :rtype: openapi.PathItem
        """
        path_parameters = self.get_path_parameters(path, view_cls)

        # 移除get参数中与path_parameters重复的项
        if operations.get("get"):
            paths_params = [param["name"] for param in path_parameters]
            query_params = []
            for path_param in operations["get"]["parameters"]:
                if path_param.name not in paths_params:
                    query_params.append(path_param)
            operations["get"]["parameters"] = query_params
        return openapi.PathItem(parameters=path_parameters, **operations)
