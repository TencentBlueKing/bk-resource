# -*- coding: utf-8 -*-

import uuid

from blueapps.utils.request_provider import get_request_username
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy


class OperateRecordQuerySet(models.query.QuerySet):
    """
    批量更新时写入更新时间和更新者
    """

    def update(self, **kwargs):
        """
        重写ORM 更新方法
        """
        # 是否跳过更新时间或更新人，某些特殊场景下使用
        if kwargs.pop("skip_update_time", False):
            kwargs.pop("updated_at", None)
        else:
            if "updated_at" not in kwargs:
                kwargs["updated_at"] = timezone.now()

        if kwargs.pop("skip_update_user", False):
            kwargs.pop("updated_by", None)
        else:
            if "updated_by" not in kwargs:
                kwargs["updated_by"] = get_request_username()

        super().update(**kwargs)


class OperateRecordModelManager(models.Manager):
    """
    通用字段(创建人、创建时间、更新人、更新时间) model Manager
    """

    def get_queryset(self):
        """获取queryset"""
        return OperateRecordQuerySet(self.model, using=self._db)

    def create(self, *args, **kwargs):
        """创建数据 自动填写通用字段"""
        kwargs.update(
            {
                "created_at": kwargs.get("created_at") or timezone.now(),
                "created_by": kwargs.get("created_by") or get_request_username(),
                "updated_at": kwargs.get("updated_at") or timezone.now(),
                "updated_by": kwargs.get("updated_by") or get_request_username(),
            }
        )
        return super().create(*args, **kwargs)

    def bulk_create(self, objs, *args, **kwargs):
        """创建数据 自动填写通用字段"""
        for obj in objs:
            obj.created_at = obj.created_at or timezone.now()
            obj.created_by = obj.created_by or get_request_username()
            obj.updated_at = obj.updated_at or timezone.now()
            obj.updated_by = obj.updated_by or get_request_username()
        return super().bulk_create(objs, *args, **kwargs)

    def bulk_update(self, objs, *args, **kwargs):
        """更新数据 自动填写通用字段"""
        for obj in objs:
            obj.created_at = obj.created_at or timezone.now()
            obj.created_by = obj.created_by or get_request_username()
            obj.updated_at = timezone.now()
            obj.updated_by = get_request_username()
        if "fields" in kwargs:
            kwargs["fields"] = {field for field in kwargs["fields"]}
            kwargs["fields"].update({"created_at", "created_by", "updated_at", "updated_by"})
        return super().bulk_update(objs, *args, **kwargs)


class OperateRecordModel(models.Model):
    """
    需要记录操作的model父类
    自动记录创建时间/修改时间与操作者
    """

    objects = OperateRecordModelManager()
    origin_objects = models.Manager()

    created_at = models.DateTimeField(gettext_lazy("创建时间"), default=timezone.now, auto_now_add=True)
    created_by = models.CharField(gettext_lazy("创建者"), max_length=32, default="", null=True, blank=True)
    updated_at = models.DateTimeField(gettext_lazy("更新时间"), blank=True, null=True, auto_now=True)
    updated_by = models.CharField(gettext_lazy("修改者"), max_length=32, default="", blank=True, null=True)

    def save(self, *args, **kwargs):
        """
        Save the current instance. Override this in a subclass if you want to
        control the saving process.

        The 'force_insert' and 'force_update' parameters can be used to insist
        that the "save" must be an SQL insert or update (or equivalent for
        non-SQL backends), respectively. Normally, they should not be set.
        """
        operator = get_request_username()
        if not self.created_by:
            self.created_by = operator
            if "update_fields" in kwargs:
                kwargs["update_fields"] = {key for key in kwargs["update_fields"]}
                kwargs["update_fields"].update({"created_by"})

        self.updated_at = timezone.now()
        self.updated_by = operator
        if "update_fields" in kwargs:
            kwargs["update_fields"] = {key for key in kwargs["update_fields"]}
            kwargs["update_fields"].update({"updated_at", "updated_by"})

        super().save(*args, **kwargs)

    class Meta:
        """元数据定义"""

        abstract = True


class SoftDeleteQuerySet(OperateRecordQuerySet):
    """
    软删除Queryset
    """

    def delete(self):
        """
        软删除delete方法实现 根据is_deleted字段过滤
        """
        self.update(
            is_deleted=True,
            updated_by=get_request_username(),
            updated_at=timezone.now(),
        )


class SoftDeleteModelManager(OperateRecordModelManager):
    """
    默认的查询和过滤方法, 不显示被标记为删除的记录
    """

    def all(self, *args, **kwargs):  # pylint: disable=unused-argument
        """
        ORM Manager all方法重写
        """
        # 默认都不显示被标记为删除的数据
        return super(SoftDeleteModelManager, self).filter(is_deleted=False)

    def filter(self, *args, **kwargs):
        """
        ORM Manager filter方法重写
        """
        # 默认都不显示被标记为删除的数据
        if not kwargs.get("is_deleted"):
            kwargs["is_deleted"] = False
        return super(SoftDeleteModelManager, self).filter(*args, **kwargs)

    def get(self, *args, **kwargs):
        """
        ORM Manager get方法重写
        """
        # 默认都不显示被标记为删除的数据
        if not kwargs.get("is_deleted"):
            kwargs["is_deleted"] = False
        return super(SoftDeleteModelManager, self).get(*args, **kwargs)

    def get_queryset(self):
        """获取queryset"""
        return SoftDeleteQuerySet(self.model, using=self._db).filter(is_deleted=False)


class SoftDeleteModel(OperateRecordModel):
    """
    需要记录删除操作的model父类
    自动记录删除时间与删除者
    对于此类的表提供软删除
    """

    objects = SoftDeleteModelManager()

    is_deleted = models.BooleanField(gettext_lazy("是否删除"), default=False)

    def delete(self, *args, **kwargs):  # pylint: disable=unused-argument
        """
        删除方法，不会删除数据
        而是通过标记删除字段 is_deleted 来软删除
        """
        self.is_deleted = True
        self.save()

    class Meta:
        """元数据定义"""

        abstract = True


class UUIDField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.update({"default": UUIDField.get_default_value, "max_length": max(64, kwargs.get("max_length", 0))})
        super().__init__(*args, **kwargs)

    @classmethod
    def get_default_value(cls) -> str:
        return uuid.uuid1().hex
