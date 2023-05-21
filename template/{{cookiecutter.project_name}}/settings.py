# -*- coding: utf-8 -*-

import os
import sys
from warnings import warn

import environ

"""
请不要修改该文件
如果你需要对settings里的内容做修改，config/default.py 文件中 添加即可
如有任何疑问，请联系 【蓝鲸助手】
"""

# 读取环境变量文件
# 配置优先级 环境变量 -> .env文件 -> settings.py
environ.Env.read_env()

# V3判断环境的环境变量为BKPAAS_ENVIRONMENT
if "BKPAAS_ENVIRONMENT" in os.environ:
    ENVIRONMENT = os.getenv("BKPAAS_ENVIRONMENT", "dev")
# V2判断环境的环境变量为BK_ENV
else:
    PAAS_V2_ENVIRONMENT = os.environ.get("BK_ENV", "development")
    ENVIRONMENT = {
        "development": "dev",
        "testing": "stag",
        "production": "prod",
    }.get(PAAS_V2_ENVIRONMENT)
DJANGO_CONF_MODULE = "config.{env}".format(env=ENVIRONMENT)

# 预配置常量
DEPLOY_ALL_MODULE = "__all__"
DEPLOY_MODULE_ENV_KEY = "BKAPP_DEPLOY_MODULE"
MODULE_PATH = "modules"
DEFAULT_DEPLOY_MODULE = "default"
# 获取所有的模块
ALL_MODULES = [
    _path
    for _path in os.listdir(MODULE_PATH)
    if not _path.startswith("_") and os.path.isdir(os.path.join(MODULE_PATH, _path))
]
# 默认运行所有模块，根据环境变量运行
if os.getenv(DEPLOY_MODULE_ENV_KEY) == DEPLOY_ALL_MODULE:
    DEPLOY_MODULE = ALL_MODULES
else:
    DEPLOY_MODULE = [
        _module
        for _module in os.getenv(DEPLOY_MODULE_ENV_KEY, DEFAULT_DEPLOY_MODULE).split(",")
        if _module in ALL_MODULES
    ]
# 添加运行 Path
sys.path.append(os.path.join(os.getcwd(), MODULE_PATH))
for _module in DEPLOY_MODULE:
    sys.path.append(os.path.join(os.getcwd(), f"{MODULE_PATH}/{_module}"))

# settings for merge, each of them should be one of tuple, list, set
SETTINGS_FOR_MERGE = ["INSTALLED_APPS"]


def load_settings(module_path: str, raise_exception: bool = True):
    try:
        module = __import__(module_path, globals(), locals(), ["*"])
    except ImportError as err:
        msg = "Could not import config '{}' (Is it on sys.path?): {}".format(module_path, err)
        if raise_exception:
            raise ImportError(msg)
        warn(msg)
        return
    for setting in dir(module):
        if setting == setting.upper():
            if setting in SETTINGS_FOR_MERGE and setting in globals():
                # mix global setting and module setting
                globals()[setting] = (
                    *globals()[setting],
                    *(
                        _s
                        for _s in getattr(module, setting)
                        if _s not in globals()[setting]
                    )
                )
            else:
                globals()[setting] = getattr(module, setting)


load_settings(module_path=DJANGO_CONF_MODULE)
for _module in DEPLOY_MODULE:
    load_settings(module_path=f"{MODULE_PATH}.{_module}.settings", raise_exception=False)
