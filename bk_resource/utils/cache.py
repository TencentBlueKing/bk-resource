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

import functools
import json
import time
import zlib

from django.core.cache import cache, caches
from django.utils.encoding import force_bytes
from django.utils.translation import gettext

from bk_resource.base import Empty
from bk_resource.settings import bk_resource_settings
from bk_resource.utils.common_utils import count_md5
from bk_resource.utils.local import local
from bk_resource.utils.logger import logger
from bk_resource.utils.request import get_request_username

try:
    mem_cache = caches["locmem"]
except Exception:
    mem_cache = cache


class UsingCache(object):
    min_length = 15
    preset = 6
    key_prefix = "web_cache"

    def __init__(
        self,
        cache_type,
        backend_cache_type=None,
        user_related=None,
        compress=True,
        is_cache_func=lambda res: True,
        func_key_generator=lambda func: "{}.{}".format(func.__module__, func.__name__),
    ):
        """
        :param cache_type: 缓存类型
        :param user_related: 是否与用户关联
        :param compress: 是否进行压缩
        :param is_cache_func: 缓存函数，当函数返回true时，则进行缓存
        :param func_key_generator: 函数标识key的生成逻辑
        """
        self.cache_type = cache_type
        self.backend_cache_type = backend_cache_type
        self.compress = compress
        self.is_cache_func = is_cache_func
        self.func_key_generator = func_key_generator
        # 先看用户是否提供了user_related参数
        # 若无，则查看cache_type是否提供了user_related参数
        # 若都没有定义，则user_related默认为True
        if user_related is not None:
            self.user_related = user_related
        elif getattr(cache_type, "user_related", None) is not None:
            self.user_related = self.cache_type.user_related
        else:
            self.user_related = True

        self.using_cache_type = self._get_using_cache_type()
        self.local_cache_enable = bool(bk_resource_settings.LOCAL_CACHE_ENABLE)

    def _get_username(self):
        username = "backend"
        if self.user_related:
            try:
                username = get_request_username()
            except Exception:
                username = "backend"
        return username

    def _get_using_cache_type(self):
        using_cache_type = self.cache_type
        if self._get_username() == "backend":
            using_cache_type = self.backend_cache_type or self.cache_type
        if using_cache_type:
            if not isinstance(using_cache_type, CacheTypeItem):
                raise TypeError("param 'cache_type' must be an" "instance of <utils.cache.CacheTypeItem>")
        return using_cache_type

    def _cache_key(self, task_definition, args, kwargs):
        # 新增根据用户openid设置缓存key
        if self.using_cache_type:
            return "{}:{}:{}:{},{}[{}]".format(
                self.key_prefix,
                self.using_cache_type.key,
                self.func_key_generator(task_definition),
                count_md5(args),
                count_md5(kwargs),
                self._get_username(),
            )
        return None

    def get_value(self, cache_key, default=None):
        """
        新增一级内存缓存（local）。在同一个请求(线程)中，优先使用内存缓存。
        一级缓存： local（web服务单次请求中生效）
        二级缓存： cache（60s生效）
        机制：
        local (miss), cache(miss): cache <- result
        local (miss), cache(hit): local <- result
        """
        if self.local_cache_enable:
            value = getattr(local, cache_key, None)
            if value:
                return json.loads(value)

        value = mem_cache.get(cache_key, default=None) or cache.get(cache_key, default=None)
        if value is None:
            return default
        if self.compress:
            try:
                value = zlib.decompress(value)
            except Exception:
                pass
            try:
                value = json.loads(force_bytes(value))
            except Exception:
                value = default
        if value and self.local_cache_enable:
            setattr(local, cache_key, json.dumps(value))
        return value

    def set_value(self, key, value, timeout=60):
        if self.compress:
            try:
                value = json.dumps(value)
            except Exception:
                logger.exception(gettext("[Cache]不支持序列化的类型: %s"), type(value))
                return False

            if len(value) > self.min_length:
                value = zlib.compress(value.encode())

        try:
            if mem_cache is not cache:
                mem_cache.set(key, value, 60)
            cache.set(key, value, timeout)
        except Exception as e:
            try:
                from blueapps.utils import get_request

                request_path = get_request().path
            except Exception:
                request_path = ""
            # 缓存出错不影响主流程
            logger.exception(
                gettext("存缓存[key:%s]时报错：%s\n value: %r\nurl: %s"),
                key,
                e,
                value,
                request_path,
            )

    def _cached(self, task_definition, args, kwargs):
        """
        【默认缓存模式】
        先检查是否缓存是否存在
        若存在，则直接返回缓存内容
        若不存在，则执行函数，并将结果回写到缓存中
        """
        cache_key = self._cache_key(task_definition, args, kwargs)
        if cache_key:
            return_value = self.get_value(cache_key)

            if return_value is None:
                return_value = self._refresh(task_definition, args, kwargs)
        else:
            return_value = self._cacheless(task_definition, args, kwargs)
        return return_value

    def _refresh(self, task_definition, args, kwargs):
        """
        【强制刷新模式】
        不使用缓存的数据，将函数执行返回结果回写缓存
        """
        cache_key = self._cache_key(task_definition, args, kwargs)

        return_value = self._cacheless(task_definition, args, kwargs)

        # 设置了缓存空数据
        # 或者不缓存空数据且数据为空时
        # 需要进行缓存
        if self.is_cache_func(return_value):
            self.set_value(cache_key, return_value, self.using_cache_type.timeout)

        return return_value

    def _cacheless(self, task_definition, args, kwargs):
        """
        【忽略缓存模式】
        忽略缓存机制，直接执行函数，返回结果不回写缓存
        """
        # 执行真实函数
        return task_definition(*args, **kwargs)

    def __call__(self, task_definition):
        @functools.wraps(task_definition)
        def cached_wrapper(*args, **kwargs):
            return_value = self._cached(task_definition, args, kwargs)
            return return_value

        @functools.wraps(task_definition)
        def refresh_wrapper(*args, **kwargs):
            return_value = self._refresh(task_definition, args, kwargs)
            return return_value

        @functools.wraps(task_definition)
        def cacheless_wrapper(*args, **kwargs):
            return_value = self._cacheless(task_definition, args, kwargs)
            return return_value

        # 为函数设置各种调用模式
        default_wrapper = cached_wrapper
        default_wrapper.cached = cached_wrapper
        default_wrapper.refresh = refresh_wrapper
        default_wrapper.cacheless = cacheless_wrapper

        return default_wrapper


using_cache = UsingCache


class CacheTypeItem(object):
    """
    缓存类型定义
    """

    def __init__(self, key, timeout, user_related=None, label=""):
        """
        :param key: 缓存名称
        :param timeout: 缓存超时，单位：s
        :param user_related: 是否用户相关
        :param label: 详细说明
        """
        self.key = key
        self.timeout = timeout
        self.label = label
        self.user_related = user_related

    def __call__(self, timeout):
        return CacheTypeItem(self.key, timeout, self.user_related, self.label)


class InstanceCache(object):
    _instance = Empty()

    @classmethod
    def instance(cls, *args, **kwargs):
        if isinstance(cls._instance, Empty):
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.__cache = {}

    def clear(self):
        self.__cache = {}

    def set(self, key, value, seconds=0, use_round=False):
        """
        :param key:
        :param value:
        :param seconds:
        :param use_round: 时间是否需要向上取整，取整用于缓存时间同步
        :return:
        """
        if not seconds:
            timeout = 0
        else:
            if not use_round:
                timeout = time.time() + seconds
            else:
                timeout = (time.time() + seconds) // seconds * seconds
        self.__cache[key] = (value, timeout)

    def __get_raw(self, key):
        value = self.__cache.get(key)
        if not value:
            return None
        if value[1] and time.time() > value[1]:
            del self.__cache[key]
            return None
        return value

    def exists(self, key):
        value = self.__get_raw(key)
        return value is not None

    def get(self, key):
        value = self.__get_raw(key)
        return value and value[0]

    def delete(self, key):
        try:
            del self.__cache[key]
        except KeyError:
            pass
