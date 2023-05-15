# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from core.permissions import SwaggerPermission

info = openapi.Info(
    title="{{ cookiecutter.app_id }}",
    default_version="v1",
    description="{{ cookiecutter.app_id }}",
)
schema_view = get_schema_view(
    info,
    public=True,
    permission_classes=(SwaggerPermission,),
)

urlpatterns = [
    # 出于安全考虑，默认屏蔽admin访问路径。
    # 开启前请修改路径随机内容，降低被猜测命中几率，提升安全性
    path("bkadmin/", admin.site.urls),
    path("account/", include("blueapps.account.urls")),
    path("swagger/", schema_view.with_ui(cache_timeout=0), name="schema-swagger-ui"),
    path("i18n/", include("django.conf.urls.i18n")),
]

for _module in settings.DEPLOY_MODULE:
    urlpatterns.append(path(f"{_module}/", include(f"{settings.MODULE_PATH}.{_module}.urls")))
