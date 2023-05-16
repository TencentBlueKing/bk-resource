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

BK_RESOURCE = "bk_resource"
BK_RESOURCE_PACKAGES = [
    "apps",
    "base",
    "conf",
    "contrib",
    "exceptions",
    "management",
    "routers",
    "serializers",
    "settings",
    "tasks",
    "tools",
    "utils",
    "viewsets",
]

DEFAULT_DICT_OBJ_KWARGS = {"key0": "val0", "key1": "val1"}
SPLIT_DICT = {"key0": "val0"}

DEFAULT_TIMESTAMP = 1640966400
DEFAULT_DATETIME_STRING = "2022-01-01 00:00:00+0800"
DEFAULT_DATE_STRING = "2022-01-01"
DEFAULT_TIME_STRING = "00:00:00"

DEFAULT_SET = {1, 2, 3}
DEFAULT_LIST = [1, 1, 1]

DEFAULT_STR = "test"
DEFAULT_BYTES = DEFAULT_STR.encode()

DEFAULT_MESSAGE = "message"
DEFAULT_OK_TEMPLATE = {"result": True, "message": None, "msg": None}

DEFAULT_IP = "127.0.0.1"

DEFAULT_FLOAT_NUMBER = "1.1"
DEFAULT_INT_NUMBER = "1"
DEFAULT_NUMBER = 1
DEFAULT_FLOAT = 1.1
DEFAULT_ZERO_NUMBER = 0

DEFAULT_CMDLINE_ARGS = {"key1": None, "-key2": "val2", "--key3": "val3"}
DEFAULT_CMDLINE_STR = "key1  -key2 val2 --key3=val3 "

DEFAULT_SPECIAL_ARGS = '()%!^"<>&|'
DEFAULT_SPECIAL_ARGS_ESCAPE = '^(^)^%^!^^^"^<^>^&^|'

DEFAULT_CONDITION_ITEM = {
    "method": "in",
    "filter_key": "app_code",
    "sql_statement": ["test"],
}
DEFAULT_CONDITION_ITEM_FILTER = "app_code__in"

DEFAULT_REPLACE_ITEM = {"t": "1", "e": "2", "s": "3"}
DEFAULT_REPLACE_RESULT = "1231"
