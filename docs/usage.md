> BkResource 是一个 Django 项目的增强 SDK，需要先初始化一个 Django 项目，再进行 BkResource 的集成   
> BkResource 依赖 Blueapps SDK 中的部分功能，如 request 与线程绑定，非 Blueapps 开发框架项目，需要手动在 Middlewares
> 中赠加 `blueapps.middleware.request_provider.RequestProvider`，详见[Blueapps Default Settings](https://github.com/TencentBlueKing/blueapps/blob/a2bc22df54fff3ad7291a965336ca31fd99a5a50/blueapps/conf/default_settings.py#L46)

## 1. 初始化

### 1.1 安装 `bk_resource` 及其依赖包

建议在 `requirements.txt` 中指定版本，避免后续 SDK 的大版本更新导致业务不可用

```bash
pip install bk_resource
```

### 1.2 在 `INSTALLED_APPS` 中增加 `bk_resource`

```python
INSTALLED_APPS = (
    ...,
    "rest_framework",
    "bk_resource",
    "example.app0",
    ...
)
```

### 1.3 在 `settings.py` 中增加 `rest_framework` 配置

```python
REST_FRAMEWORK = {
    # 异常处理
    "EXCEPTION_HANDLER": "blueapps.contrib.drf.exception.custom_exception_handler",
    # 默认分页
    "DEFAULT_PAGINATION_CLASS": "blueapps.contrib.drf.utils.pagination.CustomPageNumberPagination",
    "PAGE_SIZE": 100,
    # 默认鉴权
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework.authentication.SessionAuthentication",),
    # 默认时间格式
    "DATETIME_FORMAT": "%Y-%m-%d %H:%M:%S",
    # 默认输入校验
    "DEFAULT_PARSER_CLASSES": ("rest_framework.parsers.JSONParser",),
    # 默认响应格式
    "DEFAULT_RENDERER_CLASSES": ("blueapps.contrib.drf.renderers.APIRenderer",),
}
```

### 1.4 项目结构(App层级)

至此，初始化已完成，可以在项目代码中使用 BkResource 的能力了，与常规 Django 项目不同，BkResource 在 `app`
层级的结构增加了 `resources.py` 文件（需要手动新建），用于存放业务逻辑，以下为目录结构

```shell
- app0
   |
   - __init__.py
   - admin.py
   - apps.py
   - models.py
   - resources.py  # 业务逻辑
   - serializers.py  # 序列化器
   - views.py  # 业务入口
   - urls.py  # URL
   - migrations
         |
         - __init__.py
```

如果业务逻辑复杂，需要分模块，可以使用包的形式声明，并在包内增加 `resources.py` 文件。

```shell
- app0
   |
   - __init__.py
   - admin.py
   - apps.py
   - models.py
   - views.py  # 业务入口
   - urls.py  # URL
   - migrations
      |
      - __init__.py
   - home
      |
      - resources.py  # 业务逻辑
      - serializers.py  # 序列化器
   - user
      | 
      - resources.py  # 业务逻辑
      - serializers.py  # 序列化器
```

## 2. Resource 使用

以下会以例子的形式展示如何新建 Resource 并使用其功能，在使用时，请按照实际情况进行调整

### 2.1 新建 Resource

在 `resources.py` 文件中，引入 `Resource`，并在 `perform_request` 函数中编写业务逻辑。

```python
from bk_resource import Resource
from blueapps.utils.request_provider import get_local_request


class UpdateUserInfoResource(Resource):
    """更新用户信息"""

    def perform_request(self, validated_request_data):
        # 获取 Request 对象
        request = get_local_request()
        # 获取 User 对象
        user = request.user
        # 获取新用户名并更新
        new_username = validated_request_data.get("new_username")
        if not new_username or len(new_username) != 12:
            raise Exception("用户名不合法")
        user.username = new_username
        user.save()
        # 响应信息
        return {
            "id": user.id,
            "username": user.username,
            "last_login": user.last_login,
        }
```

### 2.2 声明 Serializer

在 2.1 中，我们新建了一个更新用户信息的业务逻辑，但这里会出现的问题是，并没有对用户输入做校验，无法确定输入的用户名是否合法，在响应时直接返回
JSON，也不利于格式化输出，在这里，可以使用 Serializer 辅助进行输入校验和输出校验

在 `serializers.py` 文件中，新建 `UpdateUserInfoRequestSerializer` 和 `UpdateUserInfoResponseSerializer`，并完成输入和输出校验逻辑

```python
from django.contrib.auth import get_user_model
from rest_framework import serializers

USER_MODEL = get_user_model()


class UpdateUserInfoRequestSerializer(serializers.Serializer):
    new_username = serializers.CharField(label="新用户名", max_length=12, min_length=6)


class UpdateUserInfoResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = USER_MODEL
        fields = ["id", "username", "last_login"]
```

在 Resource 中声明 Serializer

```python
from bk_resource import Resource
from blueapps.utils.request_provider import get_local_request
from example.app0.serializers import UpdateUserInfoRequestSerializer, UpdateUserInfoResponseSerializer


class UpdateUserInfoResource(Resource):
    """更新用户信息"""

    # 声明输入输出使用的 Serializer
    # 声明 RequestSerializer 后，所有请求都会自动校验，validated_request_data 可以直接获取校验完成的数据
    RequestSerializer = UpdateUserInfoRequestSerializer
    # 声明 ResponseSerializer 后，所有输出会自动校验
    ResponseSerializer = UpdateUserInfoResponseSerializer

    def perform_request(self, validated_request_data):
        # 获取 Request 对象
        request = get_local_request()
        # 获取 User 对象
        user = request.user
        # 获取新用户名并更新
        new_username = validated_request_data["new_username"]
        user.username = new_username
        user.save()
        # 可以直接返回 User 对象，会按照 Serializer 自动格式化为对应的内容，当然，直接返回对应的字典格式也是可以的
        return user
```

## 3. 路由使用

### 3.1 声明 ResourceViewSet

在 BkResource 中，对 `views` 做了进一步的封装，可以理解为，`Resource` 就是常规 DRF 框架中，`ViewSet` 中的每一个方法（如list,
retrieve)，按照如下指引，可以快速声明路由。

在 `views.py` 文件中，声明使用到的路由信息

```python
from bk_resource import resource
from bk_resource.viewsets import ResourceRoute, ResourceViewSet
from example.app0.resources import UpdateUserInfoResource


# 声明 ViewSet，其中，ViewSet前方的内容会成为 url 的一部分
class UserViewSet(ResourceViewSet):
    # 声明所有方法
    # Resource 会自动查找所有的子类并添加到 resource 中
    # 映射关系为 underscore_to_camel; 即 UpdateUserInfo => update_user_info
    resource_routes = [
        # 在这一条路由中，example.app0 为 APP 名，update_user_info 为 app0 下 resources.py 文件中的 UpdateUserInfoResource 对象
        # endpoint 不填写时默认为空，映射为根路由
        ResourceRoute("POST", resource.example.app0.update_user_info, endpoint="info"),
        # 我们也可以使用常规的方式进行声明，但不推荐
        ResourceRoute("POST", UpdateUserInfoResource),
        # 如果我们涉及到了 RestFul 标准的更新、删除类型，则可以使用 pk_field 声明，会自动将 pk 添加到 validated_request_data 中
        ResourceRoute("PUT", UpdateUserInfoResource, pk_field="user_id"),
    ]
```

在 `urls.py` 文件中，增加 `urlpatterns`

```python
from bk_resource.routers import ResourceRouter
from example.app0 import views

router = ResourceRouter()
router.register_module(views)

# 这里实际声明的 urls 为 ["/user/info/", "/user/", "/user/{pk}/]
urlpatterns = router.urls
```

## 4. 运行测试

至此，已完成初步的搭建，可以启动服务并访问测试，模块的详细使用说明请参照对应模块文档

## 5. 模块文档

- [Resource(./modules/resource/README.md)](./modules/resource/README.md)
- [ResourceViewSet(./modules/resource_view_set/README.md)](./modules/resource_view_set/README.md)
- [ResourceRouter(./modules/resource_router/README.md)](./modules/resource_router/README.md)
- [BKAPIResource(./modules/bk_api_resource/README.md)](./modules/bk_api_resource/README.md)
