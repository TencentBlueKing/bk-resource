# -*- coding: utf-8 -*-

from rest_framework import serializers


class UserInfoRequestSerializer(serializers.Serializer):
    username = serializers.CharField(label="用户名")


class UserInfoResponseSerializer(serializers.Serializer):
    request_username = serializers.CharField(label="请求用户名")
    user_info = serializers.JSONField(label="用户信息")
