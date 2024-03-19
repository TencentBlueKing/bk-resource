# -*- coding: utf-8 -*-

import datetime
import logging
import os

import json_log_formatter
from django.conf import settings


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
        extra["logger"] = record.name
        extra["levelname"] = record.levelname
        extra["funcName"] = record.funcName
        extra["pathname"] = record.pathname
        extra["lineno"] = record.lineno
        extra["process"] = record.process
        extra["thread"] = record.thread
        if "asctime" not in extra:
            extra["asctime"] = datetime.datetime.now().strftime(settings.LOG_TIME_FORMAT)
        if record.exc_info:
            extra["exc_info"] = self.formatException(record.exc_info)

        return extra
