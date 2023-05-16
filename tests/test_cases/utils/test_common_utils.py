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

import copy
import datetime
import decimal
from unittest import mock

import arrow
from django.test import TestCase
from django.utils.encoding import force_str
from django.utils.functional import Promise

from bk_resource.utils.common_utils import (
    DatetimeEncoder,
    DictObj,
    convert_to_cmdline_args_str,
    dict_slice,
    escape_cmd_argument,
    float_to_str,
    get_first,
    get_list,
    get_local_ip,
    get_one,
    get_unique_list,
    ignored,
    is_backend,
    number_format,
    package_contents,
    parse_filter_condition_dict,
    proxy,
    replce_special_val,
    safe_float,
    safe_int,
    to_dict,
    today_start_timestamp,
    uniqid,
    uniqid4,
)
from tests.constants.utils.common_utils import (
    BK_RESOURCE,
    BK_RESOURCE_PACKAGES,
    DEFAULT_BYTES,
    DEFAULT_CMDLINE_ARGS,
    DEFAULT_CMDLINE_STR,
    DEFAULT_CONDITION_ITEM,
    DEFAULT_CONDITION_ITEM_FILTER,
    DEFAULT_DATE_STRING,
    DEFAULT_DATETIME_STRING,
    DEFAULT_DICT_OBJ_KWARGS,
    DEFAULT_FLOAT,
    DEFAULT_FLOAT_NUMBER,
    DEFAULT_INT_NUMBER,
    DEFAULT_LIST,
    DEFAULT_NUMBER,
    DEFAULT_REPLACE_ITEM,
    DEFAULT_REPLACE_RESULT,
    DEFAULT_SET,
    DEFAULT_SPECIAL_ARGS,
    DEFAULT_SPECIAL_ARGS_ESCAPE,
    DEFAULT_STR,
    DEFAULT_TIME_STRING,
    DEFAULT_TIMESTAMP,
    DEFAULT_ZERO_NUMBER,
    SPLIT_DICT,
)


class TestPackageContents(TestCase):
    def test(self):
        self.assertEqual(BK_RESOURCE_PACKAGES, package_contents(BK_RESOURCE))


class TestDictObj(TestCase):
    def setUp(self):
        self.obj = DictObj(DEFAULT_DICT_OBJ_KWARGS)

    def test_str(self):
        value = str(self.obj)
        keys = DEFAULT_DICT_OBJ_KWARGS.keys()
        for key in keys:
            self.assertTrue(value.find(key) != -1)

    def test_getattr(self):
        key = list(DEFAULT_DICT_OBJ_KWARGS.keys())[0]
        self.assertEqual(DEFAULT_DICT_OBJ_KWARGS[key], getattr(self.obj, key))

    def test_bool(self):
        self.assertTrue(bool(self.obj))


class TestDatetimeEncoder(TestCase):
    def setUp(self) -> None:
        self.encoder = DatetimeEncoder()

    def test_datetime(self):
        datetime_obj = datetime.datetime.fromtimestamp(DEFAULT_TIMESTAMP)
        self.assertEqual(DEFAULT_DATETIME_STRING, self.encoder.default(datetime_obj))

    def test_date(self):
        date_obj = datetime.date.fromtimestamp(DEFAULT_TIMESTAMP)
        self.assertEqual(DEFAULT_DATE_STRING, self.encoder.default(date_obj))

    def test_time(self):
        time_obj = datetime.time()
        self.assertEqual(DEFAULT_TIME_STRING, self.encoder.default(time_obj))

    def test_decimal(self):
        decimal_obj = decimal.Decimal()
        self.assertEqual(str(decimal_obj), self.encoder.default(decimal_obj))

    def test_set(self):
        set_obj = DEFAULT_SET
        self.assertEqual(list(DEFAULT_SET), self.encoder.default(set_obj))

    def test_promise(self):
        promise_obj = Promise()
        self.assertEqual(force_str(promise_obj), self.encoder.default(promise_obj))

    def test_dictobj(self):
        dictobj = DictObj()
        self.assertIsInstance(self.encoder.default(dictobj), dict)

    def test_bytes(self):
        bytes_obj = DEFAULT_BYTES
        self.assertEqual(DEFAULT_STR, self.encoder.default(bytes_obj))

    def test_other(self):
        class Other:
            ...

        with self.assertRaises(TypeError):
            self.encoder.default(Other())


class TestIgnored(TestCase):
    def test_ignored(self):
        with ignored(TypeError):
            raise TypeError

    def test_not_ignored(self):
        with self.assertRaises(ValueError):
            with ignored(TypeError):
                raise ValueError


class TestGetUniqList(TestCase):
    def test(self):
        self.assertEqual([DEFAULT_LIST[0]], get_unique_list(DEFAULT_LIST))


class TestGetTodayStartTimestamp(TestCase):
    def test(self):
        datetime_obj = arrow.get(DEFAULT_DATE_STRING).datetime
        value = today_start_timestamp(datetime_obj)
        verify_value = datetime_obj.timestamp() * 1000
        self.assertEqual(verify_value, value)


class TestDictSlice(TestCase):
    def test(self):
        self.assertEqual(SPLIT_DICT, dict_slice(DEFAULT_DICT_OBJ_KWARGS, 0, 1))


class TestGetFirst(TestCase):
    def test_get(self):
        self.assertEqual(DEFAULT_DICT_OBJ_KWARGS, get_first([DEFAULT_DICT_OBJ_KWARGS, SPLIT_DICT]))

    def test_default(self):
        self.assertEqual(DEFAULT_DICT_OBJ_KWARGS, get_first([], DEFAULT_DICT_OBJ_KWARGS))


class TestGetList(TestCase):
    def test(self):
        self.assertEqual([DEFAULT_DICT_OBJ_KWARGS], get_list(DEFAULT_DICT_OBJ_KWARGS))
        self.assertEqual([DEFAULT_DICT_OBJ_KWARGS], get_list([DEFAULT_DICT_OBJ_KWARGS]))


class TestGetOne(TestCase):
    def test(self):
        self.assertEqual(DEFAULT_LIST[0], get_one(DEFAULT_LIST))
        self.assertEqual(DEFAULT_LIST[0], get_one(DEFAULT_LIST[0]))


class TestUniqid(TestCase):
    def test(self):
        self.assertIsNotNone(uniqid())

    def test_horizontal_bar(self):
        self.assertTrue(uniqid4().find("-") != -1)


class TestGetLocalIP(TestCase):
    def test(self):
        self.assertIsNotNone(get_local_ip())


class TestNumberFormat(TestCase):
    def test_float(self):
        self.assertEqual(float(DEFAULT_FLOAT_NUMBER), number_format(DEFAULT_FLOAT_NUMBER))

    def test_float_error(self):
        error_number = "{}.{}".format(DEFAULT_FLOAT_NUMBER, DEFAULT_FLOAT_NUMBER)
        self.assertEqual(error_number, number_format(error_number))

    def test_int(self):
        self.assertEqual(int(DEFAULT_INT_NUMBER), number_format(DEFAULT_INT_NUMBER))

    def test_int_error(self):
        self.assertEqual(DEFAULT_STR, number_format(DEFAULT_STR))

    def test_raw_int(self):
        self.assertEqual(DEFAULT_NUMBER, number_format(DEFAULT_NUMBER))

    def test_zero(self):
        self.assertEqual(DEFAULT_ZERO_NUMBER, number_format(False))


class TestConvertToCmdlineArgsStr(TestCase):
    def test(self):
        self.assertEqual(DEFAULT_CMDLINE_STR, convert_to_cmdline_args_str(DEFAULT_CMDLINE_ARGS))


class TestEscapeArgument(TestCase):
    def test(self):
        self.assertEqual(DEFAULT_SPECIAL_ARGS_ESCAPE, escape_cmd_argument(DEFAULT_SPECIAL_ARGS))


class TestParseFilterCondition(TestCase):
    def test(self):
        self.assertEqual(
            (DEFAULT_CONDITION_ITEM_FILTER, DEFAULT_CONDITION_ITEM["sql_statement"]),
            parse_filter_condition_dict(DEFAULT_CONDITION_ITEM, DEFAULT_CONDITION_ITEM["filter_key"]),
        )

    def test_no_sql_statement(self):
        item = copy.deepcopy(DEFAULT_CONDITION_ITEM)
        item.pop("sql_statement")
        self.assertEqual((None, None), parse_filter_condition_dict(item, item["filter_key"]))


class TestSafeInt(TestCase):
    def test_int(self):
        self.assertEqual(int(DEFAULT_INT_NUMBER), safe_int(DEFAULT_INT_NUMBER))

    def test_float(self):
        self.assertEqual(int(DEFAULT_INT_NUMBER), safe_int(DEFAULT_FLOAT_NUMBER))

    def test_str(self):
        self.assertEqual(DEFAULT_STR, safe_int(DEFAULT_STR, DEFAULT_STR))


class TestSafeFloat(TestCase):
    def test(self):
        self.assertEqual(float(DEFAULT_FLOAT_NUMBER), safe_float(DEFAULT_FLOAT_NUMBER))

    def test_nan(self):
        self.assertIsInstance(safe_float(DEFAULT_STR), float)


class TestProxy(TestCase):
    def setUp(self) -> None:
        self.proxy = proxy(DictObj(DEFAULT_DICT_OBJ_KWARGS))

    def test(self):
        key = list(DEFAULT_DICT_OBJ_KWARGS.keys())[0]
        self.assertEqual(DEFAULT_DICT_OBJ_KWARGS[key], getattr(self.proxy, key))


class TestFloatToStr(TestCase):
    def test(self):
        self.assertEqual(DEFAULT_FLOAT_NUMBER, float_to_str(DEFAULT_FLOAT))


class TestToDict(TestCase):
    def test_dict(self):
        self.assertEqual(DEFAULT_DICT_OBJ_KWARGS, to_dict(DEFAULT_DICT_OBJ_KWARGS))

    def test_iter(self):
        self.assertEqual(DEFAULT_LIST, to_dict(DEFAULT_LIST))


class TestReplaceSpecialVal(TestCase):
    def test(self):
        self.assertEqual(
            DEFAULT_REPLACE_RESULT,
            replce_special_val(DEFAULT_STR, DEFAULT_REPLACE_ITEM),
        )


class TestIsBackend(TestCase):
    def test(self):
        self.assertTrue(is_backend())

    @mock.patch(
        "bk_resource.utils.common_utils.os.path.basename",
        mock.MagicMock(return_value=DEFAULT_STR),
    )
    def test_false(self):
        self.assertFalse(is_backend())
