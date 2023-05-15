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

from blueapps.core.exceptions import BlueException
from django.utils.translation import gettext, gettext_lazy
from rest_framework import status


class CoreException(Exception):
    code = 100
    status_code = 500
    default_detail = gettext_lazy("服务异常")

    def __init__(self, message=None, data=None, code=None):
        """
        :param message: 错误信息
        :param data: 错误数据
        :param code: 错误码
        """
        if message is None:
            message = self.default_detail
        self.detail = message
        self.message = message

        if data is not None:
            self.data = data

        if code is not None:
            self.code = code

    def __str__(self):
        return str(self.message)


class APIRequestError(CoreException):
    code = 101
    message = gettext_lazy("API请求错误")

    def __init__(self, module_name: str = "", url: str = "", status_code: int = None, result=None):
        """
        :param result: 错误消息
        """
        if not isinstance(result, dict):
            result = {"message": result}
        if status_code:
            self.status_code = status_code
        result.update({"module_name": module_name, "url": url})

        self.data = result
        self.message = result.get("message")


class CustomError(CoreException):
    code = 102
    message = gettext_lazy("未知错误")


class DrfApiError(CoreException):
    code = 103
    message = gettext_lazy("REST API返回错误")

    @staticmethod
    def drf_error_processor(detail):
        """
        将DRF ValidationError 错误信息转换为字符串
        """
        if isinstance(detail, str):
            return detail
        elif isinstance(detail, dict):
            for k, v in list(detail.items()):
                if v:
                    return DrfApiError.drf_error_processor(v)
            else:
                return ""
        elif isinstance(detail, list):
            for item in detail:
                if item:
                    return DrfApiError.drf_error_processor(item)
            else:
                return ""
        else:
            return gettext("错误消息解析错误")


class HTTP404Error(CoreException):
    code = 104
    status_code = 404
    message = gettext_lazy("资源不存在")


class UserInfoMissing(CoreException):
    code = 105
    message = gettext_lazy("缺少用户信息")


class PermissionException(CoreException):
    code = 106
    status_code = 403
    default_detail = gettext_lazy("权限不足")


class ValidateException(CoreException):
    """校验失败"""

    code = 107
    default_detail = gettext_lazy("数据校验失败")


class PlatformAuthParamsNotExist(CoreException):
    code = 108
    default_detail = gettext_lazy("平台鉴权参数未配置")


class IAMNoPermission(BlueException):
    PLATFORM_CODE = "99"
    ERROR_CODE = "403"
    MESSAGE = gettext_lazy("权限不足")
    STATUS_CODE = status.HTTP_403_FORBIDDEN
