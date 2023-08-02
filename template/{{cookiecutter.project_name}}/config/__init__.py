# -*- coding: utf-8 -*-

from __future__ import absolute_import

__all__ = ["celery_app", "RUN_VER", "APP_CODE", "SECRET_KEY", "BK_URL", "BASE_DIR"]

import os

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from blueapps.core.celery import celery_app

from settings import DEPLOY_MODULE as _DEPLOY_MODULE
from settings import MODULE_PATH as _MODULE_PATH


# app 基本信息
def get_env_or_raise(key, default_value=None):
    """Get an environment variable, if it does not exist, raise an exception"""
    value = os.environ.get(key)
    if value:
        return value

    if default_value:
        return default_value

    raise RuntimeError(
        'Environment variable "{}" not found, you must set this variable to run this application.'.format(key)
    )


# 这些变量将由平台通过环境变量提供给应用，本地开发时需手动配置
APP_CODE = get_env_or_raise("BKPAAS_APP_ID", default_value=os.getenv("APP_ID"))
# 应用用于调用云 API 的 Secret
SECRET_KEY = get_env_or_raise("BKPAAS_APP_SECRET", default_value=os.getenv("APP_TOKEN"))
# SaaS运行版本，如非必要请勿修改
RUN_VER = get_env_or_raise("BKPAAS_ENGINE_REGION", default_value="default")
if RUN_VER == "default":
    RUN_VER = "open"

MODULE_PATH = _MODULE_PATH
DEPLOY_MODULE = _DEPLOY_MODULE

# 蓝鲸SaaS平台URL，例如 http://paas.bking.com
BK_URL = os.getenv("BKPAAS_URL", None)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
