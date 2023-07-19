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

from setuptools import setup

setup(
    name="bk_resource",
    version="0.4.1",
    author="blueking",
    url="https://bk.tencent.com",
    author_email="blueking@tencent.com",
    description="Bk Resource",
    packages=[
        "bk_resource",
        "bk_resource.conf",
        "bk_resource.contrib",
        "bk_resource.management",
        "bk_resource.management.commands",
        "bk_resource.utils",
    ],
    install_requires=[
        "blueapps==4.7.0rc1",
        "django>=3.2.18",
        "djangorestframework>=3.12.0",
        "drf-yasg>=1.20.0",
        "pyinstrument>=3.4.2",
        "arrow>=1.2.0",
        "django-rest-framework-condition>=0.1.1",
        "celery>=4,<5",
    ],
    include_package_data=True,
)
