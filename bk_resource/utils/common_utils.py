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

import base64
import datetime
import decimal
import hashlib
import json
import os
import pkgutil
import re
import socket
import sys
import traceback
import uuid
from collections import OrderedDict, defaultdict
from contextlib import contextmanager
from io import StringIO
from pipes import quote
from zipfile import ZipFile

from django.utils.encoding import force_str
from django.utils.functional import Promise
from django.utils.timezone import is_aware

from bk_resource.utils import time_tools
from bk_resource.utils.logger import logger

IDS_REGEX = re.compile(r"^\d+(,\d+)*$")


def package_contents(package):
    if isinstance(package, str):
        return package_contents(__import__(package, fromlist=[str("*")]))
    return [name for _, name, _ in pkgutil.iter_modules([os.path.dirname(package.__file__)])]


class DictObj(object):
    __non_zero = False

    def __init__(self, kwargs=None):
        if kwargs is None:
            kwargs = dict()
        self.__dict__.update(kwargs)
        for k, v in kwargs.items():
            if not self.__non_zero:
                self.__non_zero = True
            try:
                setattr(self, k, v)
            except AttributeError:
                msg = "[%s] attribute: `%s` has already exists, " "check your class definition `@property`" % (
                    self.__class__.__name__,
                    k,
                )
                raise AttributeError(msg)

    def __str__(self):
        return json.dumps(self.__dict__, ensure_ascii=False)

    def __getattr__(self, item):
        return self.__dict__.get(item, None)

    def __bool__(self):
        return self.__non_zero


class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return time_tools.strftime_local(obj)
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        elif isinstance(obj, datetime.time):
            if is_aware(obj):
                raise ValueError("JSON can't represent timezone-aware times.")
            r = obj.isoformat()
            if obj.microsecond:
                r = r[:12]
            return r
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        if isinstance(obj, set):
            return list(obj)
        if isinstance(obj, Promise):
            return force_str(obj)
        if issubclass(obj.__class__, DictObj):
            return obj.__dict__
        if isinstance(obj, bytes):
            return obj.decode("utf-8")
        return json.JSONEncoder.default(self, obj)


@contextmanager
def ignored(*exceptions, **kwargs):
    try:
        yield
    except exceptions:
        if kwargs.get("log_exception", True):
            logger.warning(traceback.format_exc())
        pass


def ok(message="", **options):
    result = {"result": True, "message": message, "msg": message}
    result.update(**options)
    return result


def failed(message="", **options):
    if not isinstance(message, str):
        if isinstance(message, str):
            message = message.encode()
        message = str(message)
    result = {"result": False, "message": message, "data": {}, "msg": message}
    result.update(**options)
    return result


def failed_data(message, data, **options):
    if not isinstance(message, str):
        if isinstance(message, str):
            message = message.encode()
        message = str(message)
    result = {"result": False, "message": message, "data": data, "msg": message}
    result.update(**options)
    return result


def ok_data(data=None, **options):
    if data is None:
        data = {}
    result = {"result": True, "message": "", "data": data, "msg": ""}
    result.update(**options)
    return result


def get_unique_list(_list):
    """
    list去重，并保持原有数据顺序
    :param _list:
    :return:
    """
    return list(OrderedDict.fromkeys(_list))


def today_start_timestamp(the_day=None):
    if the_day is None:
        the_day = datetime.date.today()
    if isinstance(the_day, datetime.datetime):
        the_day = the_day.date()
    days = (the_day - datetime.date(1970, 1, 1)).days
    return days * 3600 * 24 * 1000


def dict_slice(adict, start, end):
    """
    字典切片
    :param adict:
    :param start:
    :param end:
    """
    keys = list(adict.keys())
    dict_slice = {}
    for k in keys[start:end]:
        dict_slice[k] = adict[k]
    return dict_slice


def get_first(objs, default=""):
    """get the first element in a list or get blank"""
    if len(objs) > 0:
        return objs[0]
    return default


def get_list(obj):
    return obj if isinstance(obj, list) else [obj]


def get_one(obj):
    return obj[0] if isinstance(obj, (list, tuple)) else obj


def uniqid():
    # 不带横杠
    return uuid.uuid3(uuid.uuid1(), uuid.uuid4().hex).hex


def uniqid4():
    # 带横杠
    return str(uuid.uuid4())


def file_read(filename):
    """
    打开utf-8编码文件
    """
    with open(filename) as f:
        return f.read()


def file_md5sum(file):
    """
    计算文件的md5值
    """
    # 文件指针指向开头
    file.seek(0, 0)

    md5 = hashlib.md5()
    for chunk in file.chunks():
        md5.update(chunk)

    file.seek(0, 0)
    return md5.hexdigest()


def file_rename(file, new_file_name=None):
    """
    文件重命名，保留后缀
    :param file: 文件
    :param new_file_name: 新文件名，没有则默认取文件的md5
    :return: 新文件名
    """
    new_file_name = new_file_name or file_md5sum(file)
    ext = ""
    if "." in file.name:
        ext = file.name.split(".")[-1]

    if ext:
        new_file_name = "{}.{}".format(new_file_name, ext)
    return new_file_name


def tree():
    return defaultdict(tree)


def _count_md5(content):
    if content is None:
        return None
    m2 = hashlib.md5()
    if isinstance(content, str):
        m2.update(content.encode("utf8"))
    else:
        m2.update(content)
    return m2.hexdigest()


def count_md5(content, dict_sort=True):
    if dict_sort and isinstance(content, dict):
        # dict的顺序受到hash的影响，所以这里先排序再计算MD5
        return count_md5([(str(k), count_md5(content[k])) for k in sorted(content.keys())])
    elif isinstance(content, (list, tuple)):
        content = sorted([count_md5(k) for k in content])
    return _count_md5(str(content))


def get_md5(content):
    if isinstance(content, list):
        return [count_md5(c) for c in content]
    else:
        return count_md5(content)


REG_SPLIT_LIST = re.compile(r"\s*[;,]\s*")


def split_list(raw_string):
    if isinstance(raw_string, (tuple, list, set)):
        return raw_string
    return [x for x in REG_SPLIT_LIST.split(raw_string) if x]


def get_local_ip():
    """
    Returns the actual ip of the local machine.
    This code figures out what source address would be used if some traffic
    were to be sent out to some well known address on the Internet. In this
    case, a Google DNS server is used, but the specific address does not
    matter much.  No traffic is actually sent.

    stackoverflow上有人说用socket.gethostbyname(socket.getfqdn())
    但实测后发现有些机器会返回127.0.0.1
    """
    try:
        csock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        csock.connect(("8.8.8.8", 80))
        (addr, port) = csock.getsockname()
        csock.close()
        return addr
    except socket.error:
        return "127.0.0.1"


def number_format(v):
    try:
        # 字符型转为数值型 其他保持不变
        if isinstance(v, str):
            if v.find(".") > -1:
                try:
                    return float(v)
                except:  # noqa
                    return v
            else:
                try:
                    return int(v)
                except:  # noqa
                    return v
        elif v:
            return v
        else:
            return 0
    except Exception as e:
        raise Exception(e)


def convert_to_cmdline_args_str(kv_dict):
    """
    命令行参数组装
    :param kv_dict: 参数key-value对
    {
        "version": None,
        "-s": "xxx",
        "--some": "yyy",
    }
    :return:
    """
    result = ""
    for k, v in list(kv_dict.items()):
        if v:
            # 进行shell转义
            v = quote(v)
        else:
            v = ""
        if k.startswith("--"):
            result += "{}={} ".format(k, v)
        else:
            result += "{} {} ".format(k, v)
    return result


def escape_cmd_argument(arg):
    # Escape the argument for the cmd.exe shell.
    # First we escape the quote chars to produce a argument suitable for
    # CommandLineToArgvW. We don't need to do this for simple arguments.

    # if not arg or re.search(r'(["\s])', arg):
    #     arg = '"' + arg.replace('"', r'\"') + '"'

    meta_chars = '()%!^"<>&|'
    meta_re = re.compile("(" + "|".join(re.escape(char) for char in list(meta_chars)) + ")")
    meta_map = {char: "^%s" % char for char in meta_chars}

    def escape_meta_chars(m):
        char = m.group(1)
        return meta_map[char]

    return meta_re.sub(escape_meta_chars, arg)


def extract_zip(input_zip):
    """
    解压文件，获取文件列表
    """
    input_zip = ZipFile(input_zip)
    return {name: StringIO(input_zip.read(name)) for name in input_zip.namelist()}


def convert_img_to_base64(image, format="PNG"):
    """
    :param image: Image图片对象
    :param format: 保存格式
    :return: base64 string
    """
    img_buffer = StringIO()
    image.save(img_buffer, format=format, quality=95)
    base64_value = base64.b64encode(img_buffer.getvalue())
    return "data:image/{format};base64,{value}".format(format=format.lower(), value=base64_value)


def parse_filter_condition_dict(settings_condition_item, filter_key):
    if "method" in settings_condition_item:
        filter_key = "{}__{}".format(filter_key, settings_condition_item["method"])
    if "sql_statement" not in settings_condition_item:
        return None, None
    return filter_key, settings_condition_item["sql_statement"]


def safe_int(int_str, dft=0):
    try:
        int_val = int(int_str)
    except Exception:
        try:
            int_val = int(float(int_str))
        except Exception:
            int_val = dft
    return int_val


def safe_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return float("nan")


def proxy(obj):
    class Proxy(object):
        def __getattribute__(self, item):
            return getattr(obj, item)

    return Proxy()


# create a new context for this task
ctx = decimal.Context()

# 20 digits should be enough for everyone :D
ctx.prec = 20


def float_to_str(f):
    """
    Convert the given float to a string,
    without resorting to scientific notation
    """
    d1 = ctx.create_decimal(repr(f))
    return format(d1, "f")


def to_dict(obj):
    """
    python 对象递归转成字典
    """
    if isinstance(obj, dict):
        data = {}
        for (k, v) in list(obj.items()):
            data[k] = to_dict(v)
        return data
    elif hasattr(obj, "__iter__") and not isinstance(obj, str):
        return [to_dict(v) for v in obj]
    elif hasattr(obj, "__dict__"):
        data = {}
        for key in dir(obj):
            value = getattr(obj, key)
            if not key.startswith("_") and not callable(value):
                data[key] = to_dict(value)
        return data
    else:
        return obj


def replce_special_val(s, replace_dict):
    """
    替换特殊变量
    :param s: 待替换字符串
    :param replace_dict: 替换映射
    :return: 替换结果
    """
    for key, value in replace_dict.items():
        s = s.replace(key, value)
    return s


def is_backend():
    basename = os.path.basename(sys.argv[0])

    # 非web请求
    if any(
        [
            "manage.py" == basename and "runserver" not in sys.argv and "runsslserver" not in sys.argv,
            "celery" in sys.argv,
            "test" in sys.argv,
            "migrate" in sys.argv,
            basename in ["django_test_manage.py", "pydevconsole.py"],
            basename.find("pytest") != -1,
        ]
    ):
        return True

    return False
