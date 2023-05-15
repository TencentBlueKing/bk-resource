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

import logging
from typing import Callable, Dict, Generic, Optional, TypeVar, cast

logger = logging.getLogger(__name__)


class Teapot:
    def __init__(self, factory: "GenericFactory"):
        self.__factory = factory

    def __getattr__(self, name: str):
        factory = self.__factory
        raise NotImplementedError(f"I'm a teapot from factory {factory.name}, I don't have {name}")


T_Type = TypeVar("T_Type")
T_Value = TypeVar("T_Value")
T_Instance = TypeVar("T_Instance")


class GenericFactory(Generic[T_Type, T_Value]):
    """
    通用泛型工厂实现

    >>> class MockType(Enum):
    ...     Registered = "A"
    ...     NotRegister = "B"

    >>> factory: Factory[MockType, str] = Factory("testing", "")
    """

    factory_type = "generic"

    def __init__(self, name: str, defaults: Optional[T_Value] = None, allow_overwrite: bool = False):
        self.values: Dict[Optional[T_Type], T_Value] = {}
        self.allow_overwrite = allow_overwrite
        self.name = name

        if defaults is None:
            self.defaults = cast(T_Value, Teapot(self))
        else:
            self.defaults = defaults

    def replace_defaults(self, defaults: T_Value) -> T_Value:
        """
        替换默认值，返回旧值
        """

        if not self.allow_overwrite:
            raise RuntimeError(f"default value of {self.factory_type} factory {self.name} already exists")

        logger.info("replace defaults of %s factory %s", self.factory_type, self.name)

        legacy_instance = self.defaults
        self.defaults = defaults
        return legacy_instance

    def register(self, typ: T_Type, value: T_Value):
        """
        注册类型

        :raises RuntimeError: 如果类型已经注册，且不允许覆盖
        """

        if typ in self.values and not self.allow_overwrite:
            raise RuntimeError(f"{typ} of {self.factory_type} factory {self.name} already exists")

        logger.info("register %s of %s factory %s", typ, self.factory_type, self.name)
        self.values[typ] = value

    def get(self, typ: Optional[T_Type] = None) -> T_Value:
        """获取指定类型的值，如果不存在则返回默认值"""

        return self.values.get(typ, self.defaults)

    def must_get(self, typ: T_Type) -> T_Value:
        """
        获取指定类型的值，如果不存在则抛出异常

        :raises RuntimeError: 如果未注册
        """

        if typ not in self.values:
            raise RuntimeError(f"{typ} of {self.factory_type} factory {self.name} not exists")

        return self.values[typ]

    def is_support(self, typ: T_Type) -> bool:
        """是否支持该类型"""

        return typ in self.values

    def clear(self):
        """清空注册的类型"""

        logger.warning("%s factory %s cleared", self.factory_type, self.name)
        self.values.clear()

    def __getitem__(self, key: T_Type) -> T_Value:
        """按下标获取类型的值，相当于 self.must_get(key)"""
        return self.must_get(key)


class SingletonFactory(Generic[T_Type, T_Instance], GenericFactory[T_Type, T_Instance]):
    """实例工厂类，用于注册已经初始化的实例对象"""

    factory_type = "singleton"

    def __call__(self, typ: Optional[T_Type] = None) -> T_Instance:
        """获取指定类型的实例，相当于 self.get(typ)"""
        return self.get(typ)


class SimpleFactory(Generic[T_Type, T_Instance], GenericFactory[T_Type, Callable[..., T_Instance]]):
    """简单工厂类，用于注册创建实例的回调函数"""

    factory_type = "simple"

    def make(self, typ: T_Type, *args, **kwargs) -> T_Instance:
        """构造对应类型的实例"""

        callback = self.get(typ)

        return callback(*args, **kwargs)

    def must_make(self, typ: T_Type, *args, **kwargs) -> T_Instance:
        """构造对应类型的实例，如果不存在则抛出异常"""

        callback = self.must_get(typ)

        return callback(*args, **kwargs)

    def __call__(self, typ: Optional[T_Type] = None, *args, **kwargs) -> T_Instance:
        """构造对应类型的实例"""

        callback = self.get(typ)

        return callback(*args, **kwargs)
