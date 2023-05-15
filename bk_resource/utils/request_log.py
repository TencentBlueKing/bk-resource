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
import json
from datetime import datetime

from bk_resource.settings import bk_resource_settings
from bk_resource.utils.logger import logger


class BaseRequestLogHandler:
    def __init__(
        self,
        resource_name: str,
        start_time: datetime,
        end_time: datetime,
        request_data: any,
        response_data: any,
    ):
        self.resource_name = resource_name
        self.start_time = start_time
        self.end_time = end_time
        self.request_data = self.parse_json(request_data)
        self.response_data = self.parse_json(response_data)
        if bk_resource_settings.REQUEST_LOG_SPLIT_LENGTH:
            log_length = len(self.response_data)
            self.response_data = self.response_data[: bk_resource_settings.REQUEST_LOG_SPLIT_LENGTH] + (
                "." * 6 if log_length > bk_resource_settings.REQUEST_LOG_SPLIT_LENGTH else ""
            )

    @abc.abstractmethod
    def record(self):
        ...

    @classmethod
    def parse_json(cls, data: dict) -> str:
        try:
            return json.dumps(data, ensure_ascii=False)
        except Exception:
            return str(data)


class RequestLogHandler(BaseRequestLogHandler):
    def record(self):
        msg = (
            "[ResourceRequestLog]\n"
            "AppCode => %s\n"
            "Username => %s\n"
            "Resource => %s\n"
            "StartTime => %s\n"
            "EndTime => %s\n"
            "RequestData => %s\n"
            "ResponseData => %s"
        )
        logger.info(
            msg,
            self.get_app_code(),
            self.get_username(),
            self.resource_name,
            self.start_time,
            self.end_time,
            self.request_data,
            self.response_data,
        )

    @classmethod
    def get_username(cls) -> str:
        """获取请求用户名"""
        from blueapps.utils.request_provider import get_local_request

        try:
            return get_local_request().user.username
        except (IndexError, AttributeError):
            return ""

    @classmethod
    def get_app_code(cls) -> str:
        """获取AppCode"""
        from blueapps.utils.request_provider import get_local_request

        try:
            app = get_local_request().app
            return f"{app.bk_app_code}{'' if app.verified else '(unverified)'}"
        except (IndexError, AttributeError):
            return ""
