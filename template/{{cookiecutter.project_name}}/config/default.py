# -*- coding: utf-8 -*-

from distutils.util import strtobool

from blueapps.conf.default_settings import *  # noqa
from blueapps.conf.log import get_logging_config_dict

# 请在这里加入你的自定义 APP
INSTALLED_APPS += (
    "corsheaders",
    "bk_resource",
    "rest_framework",
    "drf_yasg",
)

# 跨域中间件
MIDDLEWARE = ("corsheaders.middleware.CorsMiddleware",) + MIDDLEWARE
# 自定义中间件
MIDDLEWARE += ()

# 默认数据库自增字段
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# 所有环境的日志级别可以在这里配置
LOG_LEVEL = "INFO"

# 静态资源文件(js,css等）在APP上线更新后, 由于浏览器有缓存,
# 可能会造成没更新的情况. 所以在引用静态资源的地方，都把这个加上
# Django 模板中：<script src="/a.js?v=${STATIC_VERSION}"></script>
# 如果静态资源修改了以后，上线前改这个版本号即可
STATIC_VERSION = "1.0"

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]  # noqa

# CELERY 开关，使用时请改为 True，修改项目目录下的 app_desc 文件，添加以下命令：
# worker:
#     command: python manage.py celery worker  -O fair -l info -c 4 -Q celery,default
# beat:
#     command: python manage.py celery beat -l info
# 不使用时，请修改为 False，并删除项目目录下的 app_desc 文件中 celery 配置
IS_USE_CELERY = False

# CELERY 并发数，默认为 2，可以通过环境变量或者 app_desc 设置
CELERYD_CONCURRENCY = os.getenv("BK_CELERYD_CONCURRENCY", 2)  # noqa

# CELERY 配置，申明任务的文件路径，即包含有 @task 装饰器的函数文件
CELERY_IMPORTS = ()

# load logging settings
LOG_TIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
LOGGING = get_logging_config_dict(locals())
LOGGING["formatters"]["verbose"] = {"()": "core.log.JSONLogFormatter"}
LOGGING["loggers"]["bk_resource"] = LOGGING["loggers"]["app"]
LOGGING["loggers"]["bk_audit"] = LOGGING["loggers"]["app"]
LOGGING["loggers"]["iam"] = LOGGING["loggers"]["app"]
for _l in LOGGING["loggers"].values():
    _l["propagate"] = False

# 初始化管理员列表，列表中的人员将拥有预发布环境和正式环境的管理员权限
# 注意：请在首次提测和上线前修改，之后的修改将不会生效
INIT_SUPERUSER = []

# BKUI是否使用了history模式
IS_BKUI_HISTORY_MODE = False

# 是否需要对AJAX弹窗登录强行打开
IS_AJAX_PLAIN_MODE = False

# 国际化配置
LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)  # noqa

USE_TZ = True
TIME_ZONE = "Asia/Shanghai"
LANGUAGE_CODE = "en"

LANGUAGES = (
    ("en", "English"),
    ("zh-cn", "简体中文"),
)
LANGUAGE_COOKIE_NAME = os.getenv("BKAPP_LANGUAGE_COOKIE_NAME", "blueking_language")

REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "blueapps.contrib.drf.exception.custom_exception_handler",
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_PAGINATION_CLASS": "blueapps.contrib.drf.utils.pagination.CustomPageNumberPagination",
    "PAGE_SIZE": 100,
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework.authentication.SessionAuthentication",),
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "DATETIME_FORMAT": "%Y-%m-%d %H:%M:%S",
    "NON_FIELD_ERRORS_KEY": "params_error",
    "DEFAULT_PARSER_CLASSES": ("rest_framework.parsers.JSONParser",),
    "DEFAULT_RENDERER_CLASSES": ("core.renderers.APIRenderer",),
    # 版本管理
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.URLPathVersioning",
    "DEFAULT_VERSION": "v1",
    "ALLOWED_VERSIONS": ["v1"],
    "VERSION_PARAM": "version",
}

# 平台错误代码: 7位整数，前两位表示产品代号，后5为各产品自行分配
PLATFORM_CODE = "00"

# BkResource - Swagger
SWAGGER_SETTINGS = {
    "DEFAULT_INFO": "urls.info",
    "DEFAULT_GENERATOR_CLASS": "bk_resource.utils.generators.BKResourceOpenAPISchemaGenerator",
}

# BkResource - Settings
BK_RESOURCE = {
    "REQUEST_VERIFY": bool(strtobool(os.getenv("BKAPP_API_REQUEST_VERIFY", "True"))),
    "REQUEST_LOG_SPLIT_LENGTH": int(os.getenv("BKAPP_REQUEST_LOG_SPLIT_LENGTH", 1024)),  # 请求日志截断长度，0表示不截断
    "PLATFORM_AUTH_ENABLED": bool(strtobool(os.getenv("BKAPP_PLATFORM_AUTH_ENABLED", "False"))),
    "PLATFORM_AUTH_ACCESS_TOKEN": os.getenv("BKAPP_PLATFORM_AUTH_ACCESS_TOKEN"),
    "PLATFORM_AUTH_ACCESS_USERNAME": os.getenv("BKAPP_PLATFORM_AUTH_ACCESS_USERNAME"),
    "RESOURCE_BULK_REQUEST_PROCESSES": os.getenv("BKAPP_RESOURCE_BULK_REQUEST_PROCESSES"),
}

# Cookie
SESSION_COOKIE_DOMAIN = os.getenv("BKAPP_SESSION_COOKIE_DOMAIN")
CSRF_COOKIE_DOMAIN = SESSION_COOKIE_DOMAIN
AUTH_BACKEND_DOMAIN = SESSION_COOKIE_DOMAIN

# API
APIGW_ENABLED = bool(strtobool(os.getenv("BKAPP_APIGW_ENABLED", "False")))
BK_API_URL_TMPL = os.getenv("BK_API_URL_TMPL", "") or os.getenv("BKAPP_API_URL_TMPL", "")
BK_COMPONENT_API_URL = os.getenv("BK_COMPONENT_API_URL", "") or os.getenv("BKAPP_COMPONENT_API_URL", "")

# cache
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")
REDIS_DB = os.getenv("REDIS_DB", "0")

CACHES["db"] = {
    "BACKEND": "django.core.cache.backends.db.DatabaseCache",
    "LOCATION": "django_cache",
    "OPTIONS": {"MAX_ENTRIES": 100000, "CULL_FREQUENCY": 10},
}
if REDIS_HOST:
    CACHES["redis"] = {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}",
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient", "PASSWORD": REDIS_PASSWORD},
        "KEY_PREFIX": os.getenv("REDIS_KEY_PREFIX", ""),
    }
    CACHES["default"] = CACHES["redis"]
    CACHES["login_db"] = CACHES["redis"]
else:
    CACHES["default"] = CACHES["db"]

"""
以下为框架代码 请勿修改
"""
# celery settings
if IS_USE_CELERY:
    INSTALLED_APPS = locals().get("INSTALLED_APPS", [])
    INSTALLED_APPS += (
        "django_celery_beat",
        "django_celery_results",
    )
    CELERY_ENABLE_UTC = True
    CELERY_TIMEZONE = TIME_ZONE
    CELERYBEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

# remove disabled apps
if locals().get("DISABLED_APPS"):
    INSTALLED_APPS = locals().get("INSTALLED_APPS", [])
    DISABLED_APPS = locals().get("DISABLED_APPS", [])

    INSTALLED_APPS = [_app for _app in INSTALLED_APPS if _app not in DISABLED_APPS]

    _keys = (
        "AUTHENTICATION_BACKENDS",
        "DATABASE_ROUTERS",
        "FILE_UPLOAD_HANDLERS",
        "MIDDLEWARE",
        "PASSWORD_HASHERS",
        "TEMPLATE_LOADERS",
        "STATICFILES_FINDERS",
        "TEMPLATE_CONTEXT_PROCESSORS",
    )

    import itertools

    for _app, _key in itertools.product(DISABLED_APPS, _keys):
        if locals().get(_key) is None:
            continue
        locals()[_key] = tuple([_item for _item in locals()[_key] if not _item.startswith(_app + ".")])
