# -*- coding: utf-8 -*-

from django.utils.translation import gettext as _
from rest_framework.permissions import BasePermission


class Permission(BasePermission):
    code = 403
    message = _("Permission Denied")


class IsStaffPermission(Permission):
    message = _("Staff Required")

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return False


class IsAdminPermission(Permission):
    message = _("Admin Required")

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return False


class SwaggerPermission(IsStaffPermission):
    # 为 Swagger 使用的 HtmlRenderer 做兼容，传递 Object
    message = {"message": IsStaffPermission.message}
