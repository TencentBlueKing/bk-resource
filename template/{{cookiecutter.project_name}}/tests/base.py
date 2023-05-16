# -*- coding: utf-8 -*-

from bk_resource import api as _api
from bk_resource import resource as _resource
from django.conf import settings
from django.test import TestCase as _TestCase


class TestCase(_TestCase):
    """
    Base Test Case
    """

    app_code = settings.APP_CODE
    app_secret = settings.SECRET_KEY
    resource = _resource
    api = _api
