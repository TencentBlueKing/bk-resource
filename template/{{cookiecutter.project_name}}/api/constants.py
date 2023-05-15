# -*- coding: utf-8 -*-

from enum import Enum

from django.conf import settings

ESB_PREFIX = "/api/c/compapi/v2/"
ESB_URL_FORMAT = "{}{}{{}}".format(settings.BK_COMPONENT_API_URL, ESB_PREFIX)

APIGW_URL_FORMAT = "{}/{{stage}}".format(settings.BK_API_URL_TMPL)


class APIProvider(Enum):
    APIGW = "apigw"
    ESB = "esb"
