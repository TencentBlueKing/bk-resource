# -*- coding: utf-8 -*-

import abc
import os

from bk_resource import Resource
from blueapps.account.conf import ConfFixture
from django.conf import settings

from modules.default.entry.handler import HealthzHandler


class EntryBaseResource(Resource, abc.ABC):
    tags = ["Meta"]


class HomeResource(EntryBaseResource):
    name = "首页"

    def perform_request(self, validated_request_data):
        static_url = settings.STATIC_URL.replace("http://", "//")
        app_subdomains = os.getenv("BKAPP_ENGINE_APP_DEFAULT_SUBDOMAINS", None)
        if app_subdomains:
            static_url = "//%s/static/" % app_subdomains.split(";")[0]
        data = {
            "APP_CODE": settings.APP_CODE,
            "SITE_URL": settings.SITE_URL,
            # 远程静态资源url
            "REMOTE_STATIC_URL": settings.REMOTE_STATIC_URL,
            # 静态资源
            "STATIC_URL": static_url,
            "STATIC_VERSION": settings.STATIC_VERSION,
            # 登录跳转链接
            "LOGIN_URL": ConfFixture.LOGIN_URL,
        }
        return data


class HealthzResource(EntryBaseResource):
    name = "healthz"

    def perform_request(self, validated_request_data):
        return HealthzHandler.healthz()


class PingResource(EntryBaseResource):
    name = "ping"

    def perform_request(self, validated_request_data):
        return "pong"
