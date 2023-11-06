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
from typing import Dict

import requests
from django.utils.encoding import force_str
from django.utils.translation import gettext
from requests.exceptions import HTTPError

from bk_resource.contrib.cache import CacheResource
from bk_resource.exceptions import APIRequestError
from bk_resource.settings import bk_resource_settings
from bk_resource.utils.logger import logger


class ApiResourceProtocol(metaclass=abc.ABCMeta):
    """
    API Resource Protocol
    """

    @property
    @abc.abstractmethod
    def module_name(self):
        """
        模块名
        """
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def base_url(self):
        """
        api 基本url生成规则
        """
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def action(self):
        """
        url的后缀，通常是指定特定资源
        """
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def method(self):
        """
        请求方法，仅支持GET或POST
        """
        raise NotImplementedError

    def build_url(self, validated_request_data: dict) -> str:
        raise NotImplementedError

    def build_request_data(self, validated_request_data: dict) -> dict:
        raise NotImplementedError

    def build_header(self, validated_request_data: dict) -> Dict[str, str]:
        raise NotImplementedError

    def before_request(self, context: dict) -> dict:
        raise NotImplementedError

    def parse_response(self, result: requests.Response) -> dict:
        raise NotImplementedError


class APIResource(ApiResourceProtocol, CacheResource, metaclass=abc.ABCMeta):
    """
    API类型的Resource
    """

    module_name = "default"
    TIMEOUT = 60
    IS_STANDARD_FORMAT = True
    url_keys = []

    def __init__(self, **kwargs):
        super(APIResource, self).__init__(**kwargs)
        assert self.method.upper() in ["GET", "POST", "PUT", "PATCH", "DELETE"], gettext(
            "%s method 仅支持GET或POST或PUT或PATCH或DELETE，当前为%s"
        ) % (self.module_name, self.method.upper())
        self.method = self.method.upper()
        self.session = requests.session()

    def request(self, request_data=None, **kwargs):
        request_data = request_data or kwargs
        return super(APIResource, self).request(request_data, **kwargs)

    def perform_request(self, validated_request_data):
        """
        发起http请求
        """
        validated_request_data = dict(validated_request_data)
        validated_request_data = self.build_request_data(validated_request_data)

        # 拼接最终请求的url
        request_url = self.build_url(validated_request_data)
        logger.debug("request: {}".format(request_url))

        # 构造请求头
        headers = self.build_header(validated_request_data)
        kwargs = {
            "method": self.method,
            "url": request_url,
            "timeout": self.TIMEOUT,
            "headers": headers,
            "verify": bk_resource_settings.REQUEST_VERIFY,
        }

        try:
            if self.method == "GET":
                kwargs["params"] = validated_request_data
                kwargs = self.before_request(kwargs)
                request_url = kwargs.pop("url")
                if "method" in kwargs:
                    del kwargs["method"]
                response = self.session.get(request_url, **kwargs)
            else:
                non_file_data, file_data = self.split_request_data(validated_request_data)
                if not file_data:
                    # 不存在文件数据，则按照json方式去请求
                    kwargs["json"] = non_file_data
                else:
                    # 若存在文件数据，则将非文件数据和文件数据分开传参
                    kwargs["files"] = file_data
                    kwargs["data"] = non_file_data

                kwargs = self.before_request(kwargs)
                response = self.session.request(**kwargs)
        except Exception as err:
            logger.exception(f"APIRequestFailed => {err}")
            err_message = err.__doc__ or err.__class__.__name__
            raise APIRequestError(
                module_name=self.module_name,
                url=self.action,
                result=err_message,
            ) from err
        return self.parse_response(response)

    def build_url(self, validated_request_data):
        """
        最终请求的url，可以由子类进行重写
        """
        url = self.base_url.rstrip("/") + "/" + self.action.lstrip("/")
        if self.url_keys:
            kvs = {_k: validated_request_data[_k] for _k in self.url_keys}
            url = url.format(**kvs)
        return url

    def build_request_data(self, validated_request_data):
        return validated_request_data

    def build_header(self, validated_request_data):
        """
        请求头，可以由子类重写
        """
        return {}

    def before_request(self, kwargs):
        return kwargs

    def parse_response(self, response: requests.Response):
        """
        在提供数据给response_serializer之前，对数据作最后的处理，子类可进行重写
        """
        try:
            result_json = response.json()
        except Exception as err:
            logger.exception("{} => {}".format(gettext("Response Parse Error"), err))
            result_json = response.content

        try:
            response.raise_for_status()
        except HTTPError as err:
            logger.exception(gettext("【%s】请求API错误：%s，url: %s ") % (self.module_name, err, response.request.url))
            content = str(err.response.content)
            if isinstance(result_json, dict):
                content = "[{code}] {message}".format(code=result_json.get("code"), message=result_json.get("message"))
            raise APIRequestError(
                module_name=self.module_name,
                url=self.action,
                status_code=response.status_code,
                result=content,
            )

        if not self.IS_STANDARD_FORMAT:
            return result_json

        if not isinstance(result_json, dict):
            raise APIRequestError(
                module_name=self.module_name,
                url=self.action,
                result=gettext("返回格式有误 => %s") % force_str(result_json),
            )

        if not result_json.get("result", True) and result_json.get("code") != 0:
            msg = result_json.get("message", "")
            request_id = result_json.pop("request_id", "") or response.headers.get("x-bkapi-request-id", "")
            logger.error(
                "【Module: %s】【Action: %s】(%s) get error：%s",
                self.module_name,
                self.action,
                request_id,
                msg,
                extra=dict(module_name=self.module_name, url=response.request.url),
            )
            raise APIRequestError(
                module_name=self.module_name,
                url=self.action,
                result=result_json,
            )
        return result_json.get("data")

    @staticmethod
    def split_request_data(data):
        """
        切分请求参数为文件/非文件类型，便于requests参数组装
        """
        file_data = {}
        non_file_data = {}
        for request_param, param_value in list(data.items()):
            if hasattr(param_value, "read"):
                # 一般认为含有read属性的为文件类型
                file_data[request_param] = param_value
            else:
                non_file_data[request_param] = param_value
        return non_file_data, file_data
