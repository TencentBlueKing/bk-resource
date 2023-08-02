# -*- coding: utf-8 -*-

from blueapps.account import ConfFixture
from django.conf import settings

ENTRY_DATA = {
    "APP_CODE": settings.APP_CODE,
    "SITE_URL": "/",
    "REMOTE_STATIC_URL": "/static/remote/",
    "STATIC_URL": "/static/",
    "STATIC_VERSION": "1.0",
    "LOGIN_URL": ConfFixture.LOGIN_URL
}
