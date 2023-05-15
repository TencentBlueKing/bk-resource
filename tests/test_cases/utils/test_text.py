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

from django.test import TestCase

from bk_resource.utils.text import (
    camel_to_underscore,
    convert_filename,
    cut_str_by_max_bytes,
    path_to_dotted,
    reconvert_filename,
    underscore_to_camel,
)
from tests.constants.utils.text import (
    DEFAULT_CAMEL,
    DEFAULT_DOTTED_PATH,
    DEFAULT_FILE_NAME,
    DEFAULT_MAX_BYTES,
    DEFAULT_MIN_BYTES,
    DEFAULT_PATH,
    DEFAULT_RESULT_STR,
    DEFAULT_STR,
    DEFAULT_UNDERSCORE,
    DEFAULT_VALID_FILE_NAME,
)


class TestPathToDotted(TestCase):
    def test(self):
        self.assertEqual(DEFAULT_DOTTED_PATH, path_to_dotted(DEFAULT_PATH))


class TestCamelToUnderScore(TestCase):
    def test(self):
        self.assertEqual(DEFAULT_UNDERSCORE, camel_to_underscore(DEFAULT_CAMEL))


class TestUnderScoreToCamel(TestCase):
    def test(self):
        self.assertEqual(DEFAULT_CAMEL, underscore_to_camel(DEFAULT_UNDERSCORE))


class TestConvertFileName(TestCase):
    def test(self):
        self.assertEqual(DEFAULT_VALID_FILE_NAME, convert_filename(DEFAULT_FILE_NAME))


class TestReConvertFileName(TestCase):
    def test(self):
        self.assertEqual(DEFAULT_FILE_NAME, reconvert_filename(DEFAULT_VALID_FILE_NAME))


class TestCutStr(TestCase):
    def test(self):
        self.assertEqual(DEFAULT_STR, cut_str_by_max_bytes(DEFAULT_STR, DEFAULT_MAX_BYTES))
        self.assertEqual(DEFAULT_RESULT_STR, cut_str_by_max_bytes(DEFAULT_STR, DEFAULT_MIN_BYTES))
