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

import datetime
import random

from django.test import TestCase, override_settings

from bk_resource.utils.time_tools import (
    biz2utc_str,
    biz_time_zone_offset,
    date2str,
    date_convert,
    datetime2timestamp,
    datetime_str_to_datetime,
    gen_default_time_range,
    get_datetime_list,
    get_datetime_range,
    get_timestamp_range_by_biz_date,
    hms_string,
    localtime,
    mysql_time,
    now,
    now_str,
    parse_time_compare_abbreviation,
    parse_time_range,
    strftime_local,
    timestamp2datetime,
    utc2_str,
    utc2biz_str,
    utc2localtime,
    utcoffset_in_seconds,
)
from tests.constants.utils.time_tools import (
    DEFAULT_DATE_STR,
    DEFAULT_DATETIME_FORMAT,
    DEFAULT_DATETIME_STR,
    DEFAULT_TIME_RANGE,
    DEFAULT_TIMESTAMP,
)


class TestNow(TestCase):
    def test(self):
        self.assertIsNotNone(now())


class TestNowStr(TestCase):
    def test(self):
        self.assertIsInstance(now_str(), str)


class TestLocalTime(TestCase):
    def setUp(self) -> None:
        self.now_utc = datetime.datetime.now(tz=datetime.timezone.utc)
        self.now = datetime.datetime.now()

    def test_is_aware(self):
        self.assertIsInstance(localtime(self.now_utc), datetime.datetime)

    def test_is_not_aware(self):
        self.assertIsInstance(localtime(self.now), datetime.datetime)


class TestUtc2LocalTime(TestCase):
    def test(self):
        self.assertIsInstance(utc2localtime(DEFAULT_TIMESTAMP), datetime.datetime)


class TestTimeStampToDatetime(TestCase):
    def test(self):
        self.assertIsInstance(timestamp2datetime(DEFAULT_TIMESTAMP), datetime.datetime)


class TestMySQLTime(TestCase):
    @override_settings(USE_TZ=True)
    def test_utc_time(self):
        self.assertIsInstance(mysql_time(datetime.datetime.now()), datetime.datetime)

    @override_settings(USE_TZ=True)
    def test_utc_time_with_tz(self):
        self.assertIsInstance(
            mysql_time(datetime.datetime.now(tz=datetime.timezone.utc)),
            datetime.datetime,
        )

    @override_settings(USE_TZ=False)
    def test_not_utc_time(self):
        self.assertIsInstance(mysql_time(datetime.datetime.now()), datetime.datetime)

    @override_settings(USE_TZ=False)
    def test_not_utc_time_with_tz(self):
        self.assertIsInstance(
            mysql_time(datetime.datetime.now(tz=datetime.timezone.utc)),
            datetime.datetime,
        )


class TestBizTimeZoneOffset(TestCase):
    def test(self):
        self.assertIsInstance(biz_time_zone_offset(), str)


class TestStrftimeLocal(TestCase):
    def test(self):
        self.assertIsInstance(strftime_local(datetime.datetime.now()), str)


class TestBizToUTCStr(TestCase):
    def test(self):
        self.assertIsInstance(biz2utc_str(datetime.datetime.now()), str)


class TestUTCToBizStr(TestCase):
    def test(self):
        self.assertIsInstance(utc2biz_str(datetime.datetime.now()), str)


class TestUTCToStr(TestCase):
    def test(self):
        self.assertIsInstance(utc2_str(datetime.datetime.now()), str)


class TestTimestampRangeByBizDate(TestCase):
    def test(self):
        self.assertIsInstance(get_timestamp_range_by_biz_date(str(datetime.date.today())), tuple)


class TestGetDefaultTimeRange(TestCase):
    def test(self):
        self.assertIsInstance(gen_default_time_range(0), tuple)

    def test_biz_range(self):
        self.assertIsInstance(gen_default_time_range(), tuple)


class TestParseTimeRange(TestCase):
    def test_no_range(self):
        self.assertIsInstance(parse_time_range(), tuple)

    def test_biz_range(self):
        self.assertIsInstance(parse_time_range(DEFAULT_TIME_RANGE), tuple)


class TestDateConvert(TestCase):
    def test_utc_date(self):
        self.assertIsInstance(date_convert(datetime.date.today(), _format="utc"), int)

    def test_str_date_to_datetime(self):
        self.assertIsInstance(date_convert(DEFAULT_DATETIME_STR, "datetime"), datetime.datetime)

    def test_str_date_to_date(self):
        self.assertIsInstance(date_convert(DEFAULT_DATE_STR, "date"), datetime.date)

    def test_str_date_to_utc(self):
        self.assertIsInstance(date_convert(DEFAULT_TIMESTAMP, "utc"), int)

    def test_int_date_to_datetime(self):
        self.assertIsInstance(date_convert(DEFAULT_DATETIME_STR, "datetime"), datetime.datetime)

    def test_int_date_to_date(self):
        self.assertIsInstance(date_convert(DEFAULT_DATE_STR, "date"), datetime.date)

    def test_error(self):
        self.assertEqual(date_convert(DEFAULT_DATE_STR, "utc"), "")


class TestDateToStr(TestCase):
    def test(self):
        self.assertIsInstance(date2str(datetime.date.today()), str)


class TestGetDatetimeRange(TestCase):
    def test_error(self):
        with self.assertRaises(TypeError):
            get_datetime_range("year", None)

    @override_settings(USE_TZ=False)
    def test_days_without_tz(self):
        self.assertIsInstance(get_datetime_range("day", 7), tuple)

    def test_days(self):
        self.assertIsInstance(get_datetime_range("day", 7), tuple)

    def test_hours(self):
        self.assertIsInstance(get_datetime_range("hour", 7), tuple)


class TestGetDatetimeList(TestCase):
    def setUp(self) -> None:
        self.end_time = datetime.datetime.now()
        self.begin_time = self.end_time - datetime.timedelta(days=7)

    def test_error(self):
        with self.assertRaises(TypeError):
            get_datetime_list(self.begin_time, self.end_time, "year")

    def test_day(self):
        self.assertIsInstance(get_datetime_list(self.begin_time, self.end_time, "day"), list)

    def test_hour(self):
        self.assertIsInstance(get_datetime_list(self.begin_time, self.end_time, "hour"), list)


class TestUTCOffsetInSeconds(TestCase):
    def test(self):
        self.assertIsInstance(utcoffset_in_seconds(), float)


class TestDatetimeToTimestamp(TestCase):
    def test(self):
        self.assertIsInstance(datetime2timestamp(datetime.datetime.now()), float)


class TestHmsString(TestCase):
    def test(self):
        self.assertIsInstance(hms_string(random.randint(1, 10000)), str)

    def test_zero(self):
        self.assertEqual(hms_string(0), "0s")


class TestParseTimeCompare(TestCase):
    def test(self):
        self.assertIsInstance(parse_time_compare_abbreviation(""), int)
        self.assertIsInstance(parse_time_compare_abbreviation(1), int)
        self.assertIsInstance(parse_time_compare_abbreviation("1s"), int)
        self.assertIsInstance(parse_time_compare_abbreviation("1h"), int)
        self.assertIsInstance(parse_time_compare_abbreviation("1d"), int)
        self.assertIsInstance(parse_time_compare_abbreviation("1w"), int)
        self.assertIsInstance(parse_time_compare_abbreviation("-1M"), int)
        self.assertIsInstance(parse_time_compare_abbreviation("-1y"), int)


class TestDatetimeStrToDatetime(TestCase):
    def test(self):
        self.assertIsInstance(
            datetime_str_to_datetime(DEFAULT_DATETIME_STR, DEFAULT_DATETIME_FORMAT),
            datetime.datetime,
        )
