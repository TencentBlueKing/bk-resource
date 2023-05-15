# -*- coding: utf-8 -*-

from blueapps.conf.validators import EnvValidator

from config import RUN_VER

# 环境变量检测
EnvValidator(RUN_VER).validate()

if RUN_VER == "open":
    from blueapps.patch.settings_open_saas import *  # noqa
else:
    from blueapps.patch.settings_paas_services import *  # noqa

# 本地开发环境
RUN_MODE = "DEVELOP"

LOG_LEVEL = "DEBUG"

# APP本地静态资源目录
STATIC_URL = "/static/"

# APP静态资源目录url
REMOTE_STATIC_URL = "%sremote/" % STATIC_URL

# Celery 消息队列设置 RabbitMQ
# BROKER_URL = 'amqp://guest:guest@localhost:5672//'
# Celery 消息队列设置 Redis
BROKER_URL = "redis://localhost:6379/0"

DEBUG = True

# 跨域携带Cookie
CORS_ALLOW_CREDENTIALS = True
# CSRF 无需带协议 如 *.tencent.com
CSRF_TRUSTED_ORIGINS = [origin for origin in str(os.getenv("BKAPP_CSRF_TRUSTED_ORIGINS", "")).split(",") if origin]
# 跨域 需要带协议 如 https://bk.tencent.com/
CORS_ALLOWED_ORIGINS = [origin for origin in str(os.getenv("BKAPP_CORS_ALLOWED_ORIGINS", "")).split(",") if origin]

# 多人开发时，无法共享的本地配置可以放到新建的 local_settings.py 文件中
# 并且把 local_settings.py 加入版本管理忽略文件中
try:
    from config.local_settings import *  # noqa
except ImportError:
    pass
