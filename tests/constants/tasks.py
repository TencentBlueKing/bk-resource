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

DEFAULT_PERFORM_REQUEST_USERNAME = "admin"
DEFAULT_PERFORM_REQUEST_DATA = {"username": "admin"}

QUERY_COMPLETE_RESULT = {
    "task_id": "task_id",
    "is_completed": True,
    "state": True,
    "message": None,
    "data": {"message": "message", "data": "data"},
}
QUERY_RESULT_ERROR_RESULT = {
    "task_id": "task_id",
    "is_completed": True,
    "state": True,
    "message": None,
    "data": None,
}
QUERY_CUSTOM_ERROR_RESULT = {
    "task_id": "task_id",
    "is_completed": True,
    "state": True,
    "message": "message",
    "data": "data",
}
QUERY_EXCEPTION_RESULT = {
    "task_id": "task_id",
    "is_completed": True,
    "state": True,
    "message": "message",
    "data": None,
}


class ResourceObj:
    def validate_request_data(self, data):
        return data

    def perform_request(self, data):
        return data

    def validate_response_data(self, data):
        return data
