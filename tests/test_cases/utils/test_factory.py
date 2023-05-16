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
from enum import Enum
from django.test import TestCase
import pytest

from bk_resource.utils.factory import GenericFactory, SimpleFactory, SingletonFactory


class MockType(Enum):
    Registered = "A"
    NotRegister = "B"


class TestGenericFactory(TestCase):
    """测试 GenericFactory"""

    factory: GenericFactory[MockType, str]

    @pytest.fixture(autouse=True)
    def setup(self, faker):
        self.default_value = faker.word()
        self.registered_value = faker.word()

        self.factory = GenericFactory("testing", self.default_value)
        self.factory.register(MockType.Registered, self.registered_value)

    def test_without_defaults(self):
        """测试不传入默认值"""
        factory: GenericFactory[MockType, str] = GenericFactory("testing")

        with pytest.raises(NotImplementedError):
            factory.defaults.startswith("not-implemented!")

    def test_factory_type(self):
        """测试 factory_type 默认值"""

        assert self.factory.factory_type == "generic"

    def test_allow_overwrite(self):
        """测试 allow_overwrite 默认值"""

        assert self.factory.allow_overwrite is False

    def test_replace_defaults_allow_overwrite(self):
        """测试替换默认值"""

        self.factory.allow_overwrite = True

        default_value = "b"
        assert self.factory.replace_defaults(default_value) == self.default_value
        assert self.factory.get(MockType.NotRegister) == default_value

    def test_replace_defaults_overwrite(self):
        """测试不允许覆盖时替换默认值"""

        self.factory.allow_overwrite = False

        with pytest.raises(RuntimeError):
            self.factory.replace_defaults("u-raise-me-up")

    def test_register(self):
        """测试注册"""

        assert not self.factory.is_support(MockType.NotRegister)

        self.factory.register(MockType.NotRegister, "b")

        assert self.factory.is_support(MockType.NotRegister)

    def test_register_overwrite(self):
        """测试注册不允许覆盖"""

        self.factory.allow_overwrite = False

        with pytest.raises(RuntimeError):
            self.factory.register(MockType.Registered, "b")

    def test_register_allow_overwrite(self):
        """测试注册时允许覆盖"""

        self.factory.allow_overwrite = True

        self.factory.register(MockType.Registered, "b")

    def test_get_unsupported_type(self):
        """测试获取不支持的值，返回默认值"""

        assert self.factory.get(MockType.NotRegister) == self.default_value

    def test_get_supported_type(self):
        """测试获取支持的值"""
        assert self.factory.get(MockType.Registered) == self.registered_value

    def test_get_none(self):
        """测试获取默认值"""
        assert self.factory.get() == self.default_value

    def test_must_get_unsupported_type(self):
        """测试获取不支持的值，抛出异常"""

        with pytest.raises(RuntimeError):
            self.factory.must_get(MockType.NotRegister)

    def test_must_get_supported_type(self):
        """测试获取支持的值"""
        assert self.factory.must_get(MockType.Registered) == self.registered_value

    def test_is_support(self):
        """测试是否支持该类型"""

        assert self.factory.is_support(MockType.Registered)
        assert not self.factory.is_support(MockType.NotRegister)

    def test_clear(self):
        """测试清空注册的值"""

        assert self.factory.is_support(MockType.Registered)

        self.factory.clear()

        assert not self.factory.is_support(MockType.Registered)

    def test_getitem_unsupported_type(self):
        """测试获取不支持的值，抛出异常"""

        with pytest.raises(RuntimeError):
            self.factory[MockType.NotRegister]

    def test_getitem_supported_type(self):
        """测试获取支持的值"""

        assert self.factory[MockType.Registered] == self.registered_value


class TestSingletonFactory:
    """测试 SingletonFactory"""

    factory: SingletonFactory[MockType, str]

    @pytest.fixture(autouse=True)
    def setup(self, faker):
        self.default_value = faker.word()
        self.registered_value = faker.word()

        self.factory = SingletonFactory("testing", self.default_value)
        self.factory.register(MockType.Registered, self.registered_value)

    def test_factory_type(self):
        """测试 factory_type 默认值"""

        assert SingletonFactory.factory_type == "singleton"

    def test_call_without_args(self):
        """测试不传入参数时，返回默认值"""

        assert self.factory() == self.default_value

    def test_call_with_supported_type(self):
        """测试传入支持的类型时，返回对应值"""

        assert self.factory(MockType.Registered) == self.registered_value

    def test_call_with_unsupported_type(self):
        """测试传入不支持的类型时，返回默认值"""

        assert self.factory(MockType.NotRegister) == self.default_value


class TestSimpleFactory:
    """测试 SimpleFactory"""

    factory: SimpleFactory[MockType, str]

    @pytest.fixture(autouse=True)
    def setup(self, faker, mocker):
        self.default_value = faker.word()
        self.registered_value = faker.word()

        self.factory = SimpleFactory("testing", mocker.MagicMock(return_value=self.default_value))
        self.factory.register(MockType.Registered, mocker.MagicMock(return_value=self.registered_value))

    def test_factory_type(self):
        """测试 factory_type 默认值"""

        assert self.factory.factory_type == "simple"
        assert self.registered_value != self.default_value

    def test_make_registered(self):
        """测试构造已注册的类型"""

        assert self.factory.make(MockType.Registered) == self.registered_value

    def test_make_unregistered(self):
        """测试构造未注册的类型，返回默认值"""

        assert self.factory.make(MockType.NotRegister) == self.default_value

    def test_must_make_registered(self):
        """测试构造已注册的类型，不抛出异常"""

        assert self.factory.must_make(MockType.Registered) == self.registered_value

    def test_must_make_unregistered(self):
        """测试构造未注册的类型，抛出异常"""

        with pytest.raises(RuntimeError):
            self.factory.must_make(MockType.NotRegister)

    def test_call_with_none(self):
        """测试不传入参数时，返回默认值"""

        assert self.factory() == self.default_value

    def test_getitem(self):
        """通过下标创建"""

        callback = self.factory[MockType.Registered]

        assert callback() == self.registered_value
