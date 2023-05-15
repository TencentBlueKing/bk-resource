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

import abc

from bk_resource.base import Resource
from bk_resource.utils.cache import CacheTypeItem, using_cache


class CacheResource(Resource, metaclass=abc.ABCMeta):
    """
    支持缓存的resource
    """

    # 缓存类型
    cache_type = None
    # 后台缓存时间
    backend_cache_type = None
    # 缓存是否与用户关联，默认关联
    cache_user_related: bool = None
    # 是否使用压缩
    cache_compress = True

    def __init__(self, *args, **kwargs):
        # 若cache_type为None则视为关闭缓存功能
        if self._need_cache_wrap():
            self._wrap_request()
        super(CacheResource, self).__init__(*args, **kwargs)

    def _need_cache_wrap(self):
        need_cache = False
        if self.cache_type is not None:
            if not isinstance(self.cache_type, CacheTypeItem):
                raise TypeError("param 'cache_type' must be an" "instance of <utils.cache.CacheTypeItem>")
            need_cache = True
        if self.backend_cache_type is not None:
            if not isinstance(self.backend_cache_type, CacheTypeItem):
                raise TypeError("param 'cache_type' must be an" "instance of <utils.cache.CacheTypeItem>")
            need_cache = True
        return need_cache

    def _wrap_request(self):
        """
        将原有的request方法替换为支持缓存的request方法
        """

        def func_key_generator(resource):
            key = "{}.{}".format(
                resource.__self__.__class__.__module__,
                resource.__self__.__class__.__name__,
            )
            return key

        self.request = using_cache(
            cache_type=self.cache_type,
            backend_cache_type=self.backend_cache_type,
            user_related=self.cache_user_related,
            compress=self.cache_compress,
            is_cache_func=self.cache_write_trigger,
            func_key_generator=func_key_generator,
        )(self.request)

    def cache_write_trigger(self, res):
        """
        缓存写入触发条件
        """
        return True
