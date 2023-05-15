# -*- coding: utf-8 -*-

import abc

from bk_resource import BkApiResource
from django.utils.translation import gettext_lazy as _

from api.domains import USER_MANAGE_URL


class UserManageResource(BkApiResource, abc.ABC):
    base_url = USER_MANAGE_URL
    module_name = "user_manage"


class RetrieveUser(UserManageResource):
    name = _("获取单个用户信息")
    tags = ["Meta"]
    action = "/retrieve_user/"
