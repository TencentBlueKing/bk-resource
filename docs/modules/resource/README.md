> Resource

## Resource 响应内容

Resource的返回值应只有唯一一种格式，即ResponseSerializer规定好的格式。建议所有作为API接口暴露的Resource提供ResponseSerializer，以生成完整的API文档

### 数据格式

在使用 blueapps 的统一 Renderer 的情况下，响应内容由 result,message,data,code 组成，Resource 返回值只需要关注数据本身，即 data 的内容，其余内容会由 Renderer 处理

```json
{
  "code": 0,
  "result": true,
  "message": "success",
  "data": {
    "username": "BlueKing"
  }
}
```

## Resource 响应值

### 单条数据

1. 符合 ResponseSerializer 格式的 dict 对象
2. ORM Model 对象（必须提供 ResponseSerializer 且 ResponseSerializer 继承自 ModelSerializer ）
3. 单个字段，如 `bool` / `dict` / `list` / `str`

原则上，Resource 不允许只返回单个数字或字符串，因为这样不符合 Restful 的接口规范，必须将数据包装成 dict 后再返回。例如：

```python
from bk_resource import Resource


# 错误
class PermissionResource(Resource):
    def perform_request(self, validated_request_data):
        return True


# 正确
class AnotherPermissionResource(Resource):
    def perform_request(self, validated_request_data):
        return {"has_permission": True}
```

### 多条数据

返回多条数据时，需要在 Resource 类中声明 `many_response = True`

1. 一个列表，列表中的每一个元素是符合 ResponseSerializer 格式的 dict 对象
2. ORM Model QuerySet（必须提供 ResponseSerializer 且 ResponseSerializer 继承自 ModelSerializer）

### 示例

#### 返回 ORM Model

```python
from bk_resource import Resource
from rest_framework import serializers
from example.app0.models import UserInfo


class UserInfoResource(Resource):
    class RequestSerializer(serializers.Serializer):
        username = serializers.CharField(required=True)

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = UserInfo
            fields = '__all__'

    def perform_request(self, validated_request_data):
        user = UserInfo.objects.get(username=validated_request_data["username"])
        return user
```

## Serializer 使用

### Serializer 的内嵌定义风格 （推荐使用）

若 Serializer 无复用性，则可写为内嵌类

```python
from bk_resource import Resource
from rest_framework import serializers


class UpdateUserInfoResource(Resource):
    class RequestSerializer(serializers.Serializer):
        first_name = serializers.CharField(required=True, label="名")
        last_name = serializers.CharField(required=True, label="姓")

    class ResponseSerializer(serializers.Serializer):
        full_name = serializers.CharField(required=True, label="全名")

    def perform_request(self, validated_request_data):
        full_name = "{first_name} {last_name}".format(**validated_request_data)
        return {"full_name": full_name}
```

### Serializer 的声明定义风格

若 Serializer 具有复用性，可以导入后进行声明

```python
from bk_resource import Resource
from example.app0.serializers import UpdateUserInfoRequestSerializer, UpdateUserInfoResponseSerializer


class UpdateUserInfoResource(Resource):
    RequestSerializer = UpdateUserInfoRequestSerializer
    ResponseSerializer = UpdateUserInfoResponseSerializer

    def perform_request(self, validated_request_data):
        new_username = validated_request_data["new_username"]
        return {"new_username": new_username}
```

### Serializer 的自动查找

通过配置 Resource 的 `serializers_module` 属性，Resource 将自动查找命名规则匹配的 RequestSerializer 和
ResponseSerializer，当 resources.py 中定义了大量 Resource 时，这种引入方法则显得更加优雅。(需要注意的是，此类方法定义的
Serializer 无法自动注册为 Swagger 的请求与响应示例)   
命名规则：Resource 名称去掉 `Resource` 字符串后，拼接 `RequestSerializer`/`ResponseSerializer`
，具体可以查看 `bk_resource.base.Resource._search_serializer_class` 的逻辑

```python
import abc
from bk_resource import Resource
from example.app0 import serializers


class QuickStartResource(Resource, abc.ABC):
    serializers_module = serializers


class NameGeneratorResource(QuickStartResource):
    def perform_request(self, validated_request_data):
        full_name = "{first_name} {last_name}".format(**validated_request_data)
        return {"full_name": full_name}
```

## Resource 的调用

### 导入对应 Resource 后调用

若需要在代码中调用 Resource 的业务逻辑，先创建对应的 resource 实例，再调用其 request 方法，并传入请求参数

```python
from example.app0.resources import UpdateUserInfoResource

update_user_info = UpdateUserInfoResource()

# 传入字典类型参数
update_user_info.request({"new_username": "BlueKing"})
# {"id": 1, "username": "BlueKing", "last_login": "2022-01-01 00:00:00"}

# 传入Kwargs类型参数
update_user_info.request(new_username="BlueKing")
# {"id": 1, "username": "BlueKing", "last_login": "2022-01-01 00:00:00"}
```

除了调用 `request` 方法外，也可以直接调用类本身

```python
from example.app0.resources import UpdateUserInfoResource

update_user_info = UpdateUserInfoResource()

# 传入字典类型参数
update_user_info({"new_username": "BlueKing"})
# {"id": 1, "username": "BlueKing", "last_login": "2022-01-01 00:00:00"}

# 传入Kwargs类型参数
update_user_info(new_username="BlueKing")
# {"id": 1, "username": "BlueKing", "last_login": "2022-01-01 00:00:00"}
```

若需要在代码中调用 Resource 的业务逻辑，先创建对应的 resource 实例，再调用其 request 方法，并传入请求参数

### 导入 resource 统一入口后调用

在应用启动后，按照规范注册的所有的 Resource 类，都会被自动挂载到 `resource` 上，可以直接进行调用。
这里的转换规则为，`resource.{包名}.{小写下划线分割的类名}`，如果有多层包，都需要写出来，即 `resource.{包名}.{包名}.…….{包名}.{小写下划线分割的类名}`，类名的转换规则可以查看 `bk_resource.management.root.ResourceShortcut._setup`

```python
from bk_resource import resource

# 传入字典类型参数
resource.app0.update_user_info({"new_username": "BlueKing"})
# {"id": 1, "username": "BlueKing", "last_login": "2022-01-01 00:00:00"}

# 传入Kwargs类型参数
resource.app0.update_user_info(new_username="BlueKing")
# {"id": 1, "username": "BlueKing", "last_login": "2022-01-01 00:00:00"}
```

## Resource 的批量请求

Resource 提供了 `bulk_request` 方法，基于多线程实现的批量请求方法，对于执行 I/O 密集型的业务逻辑特别有效。

```python
# 声明 Resource

import requests
from bk_resource import Resource


class IoIntensiveResource(Resource):
    def perform_request(self, validated_request_data):
        result = requests.get('https://bk.tencent.com/', params=validated_request_data)
        return result.json()
```

```python
# 实际调用

params_list = [
    {"id", 1},
    {"id", 2},
    {"id", 3},
    {"id", 4},
    # ...   
]

resource = IoIntensiveResource()

# 错误的做法
result = []
for params in params_list:
    result.append(resource(params))

# 正确的做法
result = resource.bulk_request(params_list)
```
