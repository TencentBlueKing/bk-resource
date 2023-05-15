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

from django.db.models import CharField, Model, TextChoices
from rest_framework import serializers

SERIALIZER_ERROR_MESSAGE = "(Char field) 这个字段是必填项。"


class ChoiceFieldChoices(TextChoices):
    CHOICE0 = "0", "choice0"


class Test(Model):
    test = CharField(max_length=1)

    class Meta:
        abstract = True


class UserInfoSerializer(serializers.Serializer):
    read_only_field = serializers.IntegerField(read_only=True)
    char_field = serializers.CharField()
    list_field = serializers.ListField(child=serializers.CharField())
    serializer_field = serializers.Serializer()
    related_field = serializers.RelatedField(queryset=Test)
    choice_field = serializers.ChoiceField(choices=ChoiceFieldChoices.choices)
    bool_field = serializers.BooleanField()
    float_field = serializers.FloatField()
    int_field = serializers.IntegerField()
    json_field = serializers.JSONField()


DEFAULT_SCHEMA_RESULT = [
    {
        "type": "String",
        "required": True,
        "name": "char_field",
        "source_name": "char_field",
        "description": "Char field",
    },
    {
        "type": "Array",
        "items": {
            "type": "String",
            "required": True,
            "name": "",
            "source_name": "",
            "description": "",
        },
        "required": True,
        "name": "list_field",
        "source_name": "list_field",
        "description": "List field",
    },
    {
        "type": "Object",
        "properties": {},
        "required": True,
        "name": "serializer_field",
        "source_name": "serializer_field",
        "description": "Serializer field",
    },
    {
        "type": "String",
        "required": True,
        "name": "related_field",
        "source_name": "related_field",
        "description": "Related field",
    },
    {
        "type": "Enum",
        "choices": ["0"],
        "required": True,
        "name": "choice_field",
        "source_name": "choice_field",
        "description": "Choice field",
    },
    {
        "type": "Boolean",
        "required": True,
        "name": "bool_field",
        "source_name": "bool_field",
        "description": "Bool field",
    },
    {
        "type": "Number",
        "required": True,
        "name": "float_field",
        "source_name": "float_field",
        "description": "Float field",
    },
    {
        "type": "Integer",
        "required": True,
        "name": "int_field",
        "source_name": "int_field",
        "description": "Int field",
    },
    {
        "type": "String",
        "required": True,
        "name": "json_field",
        "source_name": "json_field",
        "description": "Json field",
    },
]

DEFAULT_RENDER_LIST = [
    "{String} char_field Char field",
    "{String[]} list_field List field",
    "{Object} serializer_field Serializer field",
    "{String} related_field Related field",
    '{String="0"} choice_field Choice field',
    "{Boolean} bool_field Bool field",
    "{Number} float_field Float field",
    "{Integer} int_field Int field",
    "{String} json_field Json field",
]
