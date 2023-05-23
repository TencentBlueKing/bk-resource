# -*- coding: utf-8 -*-

from django.conf import settings

from api.constants import APIGW_URL_FORMAT, ESB_URL_FORMAT, APIProvider


def get_endpoint(api_name, provider=APIProvider.APIGW, stage=None):
    """
    获取BK-API endpoint
    """
    # 默认环境
    if not stage:
        stage = "prod" if settings.RUN_MODE == "PRODUCT" else "stag"

    # api provider
    if provider == APIProvider.ESB:
        return ESB_URL_FORMAT.format(api_name)
    return APIGW_URL_FORMAT.format(api_name=api_name, stage=stage)
