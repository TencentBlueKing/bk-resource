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

from bk_resource.exceptions import CustomError
from bk_resource.tasks import step


class AsyncResultMock(mock.MagicMock):
    data = {"message": "message", "data": "data"}

    def __init__(self, task_id):
        super().__init__()

    @property
    def info(self):
        return self.data

    @property
    def state(self):
        return True

    def successful(self):
        return True

    def failed(self):
        return False

    def get(self):
        return self.data


class AsyncResultResultFailedMock(AsyncResultMock):
    @property
    def info(self):
        return None

    def get(self):
        return None


class AsyncResultCustomErrorMock(AsyncResultMock):
    def get(self):
        raise CustomError(message="message", data="data")


class AsyncResultExceptionMock(AsyncResultMock):
    def get(self):
        raise Exception("message")


class StepObj:
    def update_state(self, state, message, data):
        ...

    @step
    def run_callable(self):
        return

    @step()
    def run_none(self):
        return
