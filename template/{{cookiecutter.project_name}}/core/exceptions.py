# -*- coding: utf-8 -*-

from blueapps.core.exceptions import BlueException
from django.utils.translation import ugettext_lazy as _


class ApiError(BlueException):
    pass


class ValidationError(BlueException):
    MESSAGE = _("参数验证失败")
    ERROR_CODE = "001"

    def __init__(self, *args, data=None, **kwargs):
        if args:
            custom_message = args[0]
            if isinstance(custom_message, tuple):
                super(ValidationError, self).__init__(custom_message[1], data=custom_message[0], **kwargs)
            else:
                super(ValidationError, self).__init__(custom_message, **kwargs)
        else:
            super(ValidationError, self).__init__(**kwargs)


class ApiResultError(ApiError):
    MESSAGE = _("远程服务请求结果异常")
    ERROR_CODE = "002"


class ComponentCallError(BlueException):
    MESSAGE = _("组件调用异常")
    ERROR_CODE = "003"


class LocalError(BlueException):
    MESSAGE = _("组件调用异常")
    ERROR_CODE = "004"


class LanguageDoseNotSupported(BlueException):
    MESSAGE = _("语言不支持")
    ERROR_CODE = "005"


class InstanceNotFound(BlueException):
    MESSAGE = _("资源实例获取失败")
    ERROR_CODE = "006"


class PermissionError(BlueException):
    MESSAGE = _("权限不足")
    ERROR_CODE = "403"


class ApiRequestError(ApiError):
    MESSAGE = _("服务不稳定，请检查组件健康状况")
    ERROR_CODE = "015"
