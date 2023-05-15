# -*- coding: utf-8 -*-

from config import RUN_VER

if RUN_VER == "open":
    from blueapps.patch.settings_open_saas import *  # noqa
else:
    from blueapps.patch.settings_paas_services import *  # noqa

# 跨域携带Cookie
CORS_ALLOW_CREDENTIALS = True
# CSRF 无需带协议 如 *.tencent.com
CSRF_TRUSTED_ORIGINS = [origin for origin in str(os.getenv("BKAPP_CSRF_TRUSTED_ORIGINS", "")).split(",") if origin]
# 跨域 需要带协议 如 https://bk.tencent.com/
CORS_ALLOWED_ORIGINS = [origin for origin in str(os.getenv("BKAPP_CORS_ALLOWED_ORIGINS", "")).split(",") if origin]

# 正式环境
RUN_MODE = "PRODUCT"
