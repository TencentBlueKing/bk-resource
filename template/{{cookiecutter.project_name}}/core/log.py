# -*- coding: utf-8 -*-

import datetime
import logging
import os

import json_log_formatter
from django.conf import settings
from rest_framework.settings import api_settings


class JSONLogFormatter(json_log_formatter.JSONFormatter):
    """
    日志格式化器
    """

    def json_record(self, message: str, extra: dict, record: logging.LogRecord) -> dict:
        from blueapps.utils.request_provider import get_or_create_local_request_id

        # 移除request
        if "request" in extra:
            request = extra.pop("request")
            extra["username"] = request.user.username
        extra["request_id"] = get_or_create_local_request_id()
        extra["bk_app_code"] = settings.APP_CODE
        extra["bk_app_module"] = os.getenv("BKPAAS_APP_MODULE_NAME", "default")
        extra["bk_run_mode"] = settings.RUN_MODE
        extra["message"] = message
        extra["name"] = record.name
        extra["level"] = record.levelname
        extra["func"] = record.funcName
        extra["path"] = record.pathname
        extra["lineno"] = record.lineno
        extra["process"] = record.process
        extra["thread"] = record.thread
        if "time" not in extra:
            extra["time"] = datetime.datetime.now().strftime(api_settings.DATETIME_FORMAT)

        if record.exc_info:
            extra["exc_info"] = self.formatException(record.exc_info)

        return extra
