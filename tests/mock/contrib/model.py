# -*- coding: utf-8 -*-
"""
TencentBlueKing is pleased to support the open source community by making
蓝鲸智云 - Resource SDK (BlueKing - Resource SDK) available.
Copyright (C) 2023 THL A29 Limited,
a Tencent company. All rights reserved.
Licensed under the MIT License (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at https://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
either express or implied. See the License for the
specific language governing permissions and limitations under the License.
We undertake not to change the open source license (MIT license) applicable
to the current version of the project delivered to anyone in the future.
"""

from django.db import models
from rest_framework import serializers

from bk_resource.contrib.model import ModelResource

DEFAULT_OBJ = {"pk": 1}


class QuerySet:
    count = 0
    items = [DEFAULT_OBJ]

    def get(self, *args, **kwargs):
        return DEFAULT_OBJ

    def __next__(self):
        try:
            item = self.items[self.count]
            self.count += 1
            return item
        except IndexError:
            raise StopIteration

    def __iter__(self):
        return self


class DeleteQuerySet(QuerySet):
    def delete(self):
        ...

    def get(self, *args, **kwargs):
        class Item:
            delete = self.delete

        return Item()


class TestManager:
    def all(self):
        return QuerySet()


class TestDeleteManager:
    def all(self):
        return DeleteQuerySet()


class Test(models.Model):
    test = models.CharField(max_length=1)

    class Meta:
        abstract = True

    objects = TestManager()


class DestroyTest(models.Model):
    test = models.CharField(max_length=1)

    class Meta:
        abstract = True

    objects = TestDeleteManager()


class SerializerClass(serializers.Serializer):
    pk = serializers.IntegerField()

    def create(self, validated_data):
        return DEFAULT_OBJ

    def update(self, instance, validated_data):
        return DEFAULT_OBJ


class ListSerializerClass(SerializerClass):
    @property
    def data(self):
        return [DEFAULT_OBJ]


class TestRetrieve(ModelResource):
    model = Test
    action = "retrieve"
    lookup_field = "pk"
    serializer_class = SerializerClass


class TestList(ModelResource):
    model = Test
    action = "list"
    serializer_class = ListSerializerClass


class TestCreate(ModelResource):
    model = Test
    action = "create"
    serializer_class = SerializerClass


class TestUpdate(ModelResource):
    model = Test
    action = "update"
    serializer_class = SerializerClass


class TestDestroy(ModelResource):
    model = DestroyTest
    action = "destroy"
