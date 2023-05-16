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

from unittest import mock

from django.test import TestCase

from bk_resource.tasks import query_task_result, run_perform_request
from tests.constants.tasks import (
    DEFAULT_PERFORM_REQUEST_DATA,
    DEFAULT_PERFORM_REQUEST_USERNAME,
    QUERY_COMPLETE_RESULT,
    QUERY_CUSTOM_ERROR_RESULT,
    QUERY_EXCEPTION_RESULT,
    QUERY_RESULT_ERROR_RESULT,
    ResourceObj,
)
from tests.mock.tasks import (
    AsyncResultCustomErrorMock,
    AsyncResultExceptionMock,
    AsyncResultMock,
    AsyncResultResultFailedMock,
    StepObj,
)


class TestRunPerformRequest(TestCase):
    def test(self):
        self.assertEqual(
            DEFAULT_PERFORM_REQUEST_DATA,
            run_perform_request(
                f"{ResourceObj.__module__}.{ResourceObj.__name__}",
                DEFAULT_PERFORM_REQUEST_USERNAME,
                DEFAULT_PERFORM_REQUEST_DATA,
            ),
        )
        self.assertEqual(
            DEFAULT_PERFORM_REQUEST_DATA,
            run_perform_request(
                ResourceObj(),
                DEFAULT_PERFORM_REQUEST_USERNAME,
                DEFAULT_PERFORM_REQUEST_DATA,
            ),
        )


class TestQueryTaskResult(TestCase):
    @mock.patch("bk_resource.tasks.AsyncResult", AsyncResultMock)
    def test_complete(self):
        self.assertEqual(QUERY_COMPLETE_RESULT, query_task_result("task_id"))

    @mock.patch("bk_resource.tasks.AsyncResult", AsyncResultResultFailedMock)
    def test_result_error(self):
        self.assertEqual(QUERY_RESULT_ERROR_RESULT, query_task_result("task_id"))

    @mock.patch("bk_resource.tasks.AsyncResult", AsyncResultCustomErrorMock)
    def test_custom_error(self):
        self.assertEqual(QUERY_CUSTOM_ERROR_RESULT, query_task_result("task_id"))

    @mock.patch("bk_resource.tasks.AsyncResult", AsyncResultExceptionMock)
    def test_exception(self):
        self.assertEqual(QUERY_EXCEPTION_RESULT, query_task_result("task_id"))


class TestStep(TestCase):
    def test_callable(self):
        StepObj().run_callable()

    def test_none(self):
        StepObj().run_none()
