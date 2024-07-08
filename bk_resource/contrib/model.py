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
from typing import Union

from django.core.handlers.wsgi import WSGIRequest
from django.db import models
from django.utils.translation import gettext
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet

from bk_resource import Resource
from bk_resource.base import Empty
from bk_resource.utils.request import get_mock_request


class ViewMixin(GenericAPIView):
    filter_fields = []
    search_fields = []
    view_set_attrs = {}

    @property
    def model(self):
        """
        关联的Django Model
        """
        raise NotImplementedError

    @property
    def queryset(self):
        """
        关联的QuerySet
        """
        if hasattr(self.model, "is_deleted"):
            return self.model.objects.filter(is_deleted=False)
        return self.model.objects.all()

    @property
    def serializer_class(self):
        """
        序列化器
        """
        raise NotImplementedError

    def build_request(self, *, method: str, params: dict) -> WSGIRequest:
        # 构造虚拟请求对象
        request = get_mock_request(REQUEST_METHOD=method)
        # 为对应的方法添加请求体
        if request.method.lower() in ["get"]:
            setattr(request, "query_params", params)
        elif request.method.lower() in ["post", "put", "patch"]:
            setattr(request, "data", params)
        return request

    def build_view_set(self, *, request: WSGIRequest = None, method: str = None, params: dict) -> ModelViewSet:
        # 构造 Request
        if request is None:
            assert method is not None, gettext("request and method cannot be empty at the same time")
            request = self.build_request(method=method, params=params)
        # 构造 ViewSet, ModelResource分页配置与ResourceViewSet冲突
        model_params = {
            "queryset": self.queryset,
            "filter_backends": self.filter_backends,
            "serializer_class": self.serializer_class,
            "pagination_class": None,
            "lookup_field": self.lookup_field,
            "kwargs": params,
            "format_kwarg": self.get_format_suffix(**params),
            "filter_fields": self.filter_fields,
            "search_fields": self.search_fields,
            "request": request,
            **self.view_set_attrs,
        }
        view_set = ModelViewSet(**model_params)
        return view_set

    def build_request_and_view_set(self, *, method: str, params: dict) -> (WSGIRequest, ModelViewSet):
        request = self.build_request(method=method, params=params)
        view_set = self.build_view_set(request=request, method=method, params=params)
        return request, view_set


class ModelResource(Resource, ViewMixin, metaclass=abc.ABCMeta):
    """
    ModelViewSet
    """

    @property
    def action(self):
        raise NotImplementedError(gettext("action not set"))

    def perform_request(self, validated_request_data: dict) -> any:
        try:
            handler = getattr(self, self.action)
        except (TypeError, AttributeError):
            raise NotImplementedError(gettext("handler of %s is not implemented") % self.action)
        return handler(validated_request_data)

    def list(self, params: dict) -> list:
        request, view_set = self.build_request_and_view_set(method="GET", params=params)
        return view_set.list(request, params).data

    def retrieve(self, params: dict) -> dict:
        request, view_set = self.build_request_and_view_set(method="GET", params=params)
        return view_set.retrieve(request, params).data

    def create(self, params: dict) -> dict:
        request, view_set = self.build_request_and_view_set(method="POST", params=params)
        return view_set.create(request, params).data

    def update(self, params: dict) -> dict:
        partial = params.pop("partial", False)
        request, view_set = self.build_request_and_view_set(method="PATCH" if partial else "PUT", params=params)
        return view_set.update(request, params, partial=partial).data

    def destroy(self, params: dict) -> None:
        request, view_set = self.build_request_and_view_set(method="DELETE", params=params)
        return view_set.destroy(request, params).data

    def get_val_from_request_data(self, request_data: Union[models.Model, dict], key: str) -> any:
        try:
            if isinstance(request_data, models.Model):
                return getattr(request_data, key)
            else:
                return request_data[key]
        except (AttributeError, KeyError):
            return Empty

    def build_extra_params(self, request_data: Union[models.Model, dict], validated_request_data: dict) -> dict:
        non_use_fields = set(self.filter_fields) - set(validated_request_data.keys())
        for field in non_use_fields:
            val = self.get_val_from_request_data(request_data, field)
            if val is Empty:
                continue
            validated_request_data[field] = val
        return validated_request_data
