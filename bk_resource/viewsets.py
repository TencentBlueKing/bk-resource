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

from typing import List

import arrow
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponseBase
from django.utils.decorators import method_decorator
from django.utils.translation import gettext
from django.views.decorators.cache import cache_control
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework_condition import condition

from bk_resource.base import Resource
from bk_resource.settings import bk_resource_settings


class ResourceRoute(object):
    """
    Resource的视图配置，应用于viewsets
    """

    def __init__(
        self,
        method,
        resource_class,
        endpoint="",
        pk_field=None,
        enable_paginate=False,
        content_encoding=None,
        decorators=None,
    ):
        """
        :param method: 请求方法，目前支持GET, POST, PUT, PATCH, DELETE
        :param resource_class: 所用到的Resource类
        :param endpoint: 端点名称，不提供则为list或create
        :param pk_field: 主键名称，如果不为空，则该视图为 detail route
        :param enable_paginate: 是否对结果进行分页
        :param content_encoding: 返回数据内容编码类型
        :params decorators: 给view_func添加的装饰器列表
        """

        self.method = method.upper()

        if isinstance(resource_class, Resource):
            resource_class = resource_class.__class__
        if not issubclass(resource_class, Resource):
            raise ValueError(gettext("resource_class参数必须提供Resource的子类, 当前类型: %s") % resource_class)

        self.resource_class = resource_class

        self.endpoint = endpoint

        self.enable_paginate = enable_paginate

        self.content_encoding = content_encoding

        self.pk_field = pk_field

        self.decorators = decorators if isinstance(decorators, list) else None


class ResourceViewSet(viewsets.GenericViewSet):
    EMPTY_ENDPOINT_METHODS = {
        "GET": "list",
        "POST": "create",
        "PUT": "update",
        "PATCH": "partial_update",
        "DELETE": "destroy",
    }

    # 用于执行请求的Resource类
    resource_routes: List[ResourceRoute] = []
    filter_backends = []

    # swagger
    if bk_resource_settings.DEFAULT_SWAGGER_SCHEMA_CLASS is not None:
        swagger_schema = bk_resource_settings.DEFAULT_SWAGGER_SCHEMA_CLASS

    def get_serializer_class(self):
        """
        获取序列化器
        """
        serializer_class = None
        for route in self.resource_routes:
            if self.action == route.endpoint:
                serializer_class = route.resource_class.RequestSerializer
                break

        if not serializer_class:
            serializer_class = Serializer

        class Meta:
            ref_name = None

        serializer_class.Meta = Meta
        return serializer_class

    def get_queryset(self):
        """
        添加默认函数，避免swagger生成报错
        """
        return

    @classmethod
    def generate_endpoint(cls):
        for resource_route in cls.resource_routes:
            # 生成方法模版
            function = cls._generate_function_template(resource_route)

            # 请求序列化
            request_serializer_class = resource_route.resource_class.RequestSerializer or Serializer
            request_serializer = request_serializer_class(many=resource_route.resource_class.many_request_data)

            # 响应序列化
            response_serializer_class = (
                resource_route.resource_class.ResponseSerializer
                or resource_route.resource_class.serializer_class
                or Serializer
            )
            # 支持使用 Field 作为 data 内容
            try:
                response_serializer = response_serializer_class(many=resource_route.resource_class.many_response_data)
            except TypeError:
                response_serializer = response_serializer_class()

            # 启用分页
            if resource_route.enable_paginate:
                paginator_response_builder = bk_resource_settings.DEFAULT_PAGINATOR_RESPONSE_BUILDER
                response_serializer = paginator_response_builder(
                    resource_class=resource_route.resource_class,
                    data_serializer=response_serializer,
                ).serializer

            # 统一响应格式
            standard_response_builder = bk_resource_settings.DEFAULT_STANDARD_RESPONSE_BUILDER
            response_serializer = standard_response_builder(
                resource_class=resource_route.resource_class,
                data_serializer=response_serializer,
            ).serializer

            decorator_function = swagger_auto_schema(
                responses={
                    200: response_serializer,
                    500: bk_resource_settings.DEFAULT_ERROR_RESPONSE_SERIALIZER,
                },
                operation_description=resource_route.resource_class.__doc__,
                request_body=request_serializer
                if resource_route.method in ["POST", "PUT", "PATCH", "DELETE"]
                else None,
                query_serializer=request_serializer if resource_route.method == "GET" else None,
                operation_summary=getattr(resource_route.resource_class, "name", None),
                tags=getattr(resource_route.resource_class, "tags", None),
                enable_paginator=resource_route.enable_paginate,
            )

            # 添加装饰器
            if resource_route.decorators:
                for decorator in resource_route.decorators:
                    function = decorator(function)

            # 为Viewset设置方法
            if not resource_route.endpoint:
                function = decorator_function(function)
                # 默认方法无需加装饰器，否则会报错
                if resource_route.method == "GET":
                    if resource_route.pk_field:
                        cls.retrieve = function
                    else:
                        cls.list = function
                elif resource_route.method == "POST":
                    if resource_route.pk_field:
                        raise AssertionError(
                            gettext("当请求方法为 %s，且 endpoint 为空时，禁止设置 pk_field 参数") % resource_route.method
                        )
                    cls.create = function
                elif resource_route.method in cls.EMPTY_ENDPOINT_METHODS:
                    if not resource_route.pk_field:
                        raise AssertionError(
                            gettext("当请求方法为 %s，且 endpoint 为空时，必须提供 pk_field 参数") % resource_route.method
                        )
                    setattr(cls, cls.EMPTY_ENDPOINT_METHODS[resource_route.method], function)
                else:
                    raise AssertionError(gettext("不支持的请求方法: %s，请确认resource_routes配置是否正确!") % resource_route.method)
            else:
                function = method_decorator(cache_control(max_age=0, private=True))(function)
                function.__name__ = resource_route.endpoint
                if resource_route.pk_field:
                    function = action(methods=[resource_route.method], detail=True)(function)
                else:
                    function = action(methods=[resource_route.method], detail=False)(function)
                function = condition(
                    etag_func=resource_route.resource_class.etag,
                    last_modified_func=resource_route.resource_class.last_modified,
                )(function)

                function = decorator_function(function)
                setattr(cls, resource_route.endpoint, function)

    @classmethod
    def _generate_function_template(cls, resource_route: ResourceRoute):
        """
        生成方法模版
        """

        def template(self, request, *args, **kwargs):
            start_time = arrow.now().datetime

            resource = resource_route.resource_class()
            request_data = request.query_params.copy() if resource_route.method == "GET" else request.data

            # 如果是detail route，需要重url参数中获取主键，并塞到请求参数中
            if resource_route.pk_field:
                request_data.update({resource_route.pk_field: kwargs[cls.lookup_field]})

            # 合并url path params
            if kwargs:
                request_data.update(kwargs)

            params = {"request_data": request_data}

            # 判断是否需要绑定request对象
            if resource.bind_request:
                params["_request"] = request

            is_async_task = "HTTP_X_ASYNC_TASK" in request.META
            if is_async_task:
                # 执行异步任务
                data = resource.delay(**params)
                response = Response(data)
            else:
                try:
                    data = resource.request(**params)
                    if isinstance(data, Response):
                        response = data
                        data = data.data
                    elif isinstance(data, HttpResponseBase):
                        response = data
                        data = getattr(data, "content", "")
                    elif resource_route.enable_paginate:
                        page = self.paginate_queryset(data)
                        response = self.get_paginated_response(page)
                    else:
                        response = Response(data)
                except ObjectDoesNotExist:
                    # 默认异常，有特殊情况在程序逻辑中处理
                    raise Exception(gettext("[%s] 访问的资源不存在") % resource_route.resource_class.__name__)

            if resource_route.content_encoding:
                response.content_encoding = resource_route.content_encoding

            end_time = arrow.now().datetime

            # 不记录日志的直接返回
            if not resource.support_data_collect:
                return response

            # 记录请求日志
            resource_name = "{}.{}".format(resource.__class__.__module__, resource.__class__.__name__)
            log_handler = bk_resource_settings.REQUEST_LOG_HANDLER
            log_handler(resource_name, start_time, end_time, request_data, data).record()

            return response

        return template
