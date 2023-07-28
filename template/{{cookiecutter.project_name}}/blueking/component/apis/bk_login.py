# -*- coding: utf-8 -*-

from blueking.component.base import ComponentAPI


class CollectionsBkLogin(object):
    """Collections of BK_LOGIN APIS"""

    def __init__(self, client):
        self.client = client

        self.get_all_users = ComponentAPI(
            client=self.client,
            method="GET",
            path="/api/c/compapi{bk_api_ver}/bk_login/get_all_users/",
            description="获取所有用户信息",
        )
        self.get_batch_users = ComponentAPI(
            client=self.client,
            method="POST",
            path="/api/c/compapi{bk_api_ver}/bk_login/get_batch_users/",
            description="批量获取用户信息",
        )
        self.get_user = ComponentAPI(
            client=self.client, method="GET", path="/api/c/compapi{bk_api_ver}/bk_login/get_user/", description="获取用户信息"
        )
        self.get_all_user = ComponentAPI(
            client=self.client,
            method="GET",
            path="/api/c/compapi{bk_api_ver}/bk_login/get_all_user/",
            description="获取所有用户信息",
        )
        self.get_batch_user = ComponentAPI(
            client=self.client,
            method="GET",
            path="/api/c/compapi{bk_api_ver}/bk_login/get_batch_user/",
            description="获取多个用户信息",
        )
        self.is_login = ComponentAPI(
            client=self.client,
            method="GET",
            path="/api/c/compapi{bk_api_ver}/bk_login/is_login/",
            description="判断用户是否登录",
        )
