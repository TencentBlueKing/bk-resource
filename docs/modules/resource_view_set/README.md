> ResourceViewSet

## ResourceViewSet

自定义的ViewSet类通过继承ResourceViewSet类实现。 在 drf_non_orm 中，视图函数已被高度抽象为基于 `ResourceRoute` 类的配置。 因此，原则上，ViewSet 类不应定义任何的视图函数，但仍支持部分原有属性配置，如鉴权配置 `permission_classes`。

```python
from bk_resource import resource
from bk_resource.viewsets import ResourceRoute, ResourceViewSet
from example.app0.resources import UpdateUserInfoResource


# 声明 ViewSet，其中，ViewSet前方的内容会成为 url 的一部分
class UserInfoViewSet(ResourceViewSet):
    # 声明所有方法
    # Resource 会自动查找所有的子类并添加到 resource 中
    # 映射关系为 underscore_to_camel; 即 UpdateUserInfo => update_user_info
    resource_routes = [
        # 在这一条路由中，app0 为 APP 名，update_user_info 为 app0 下 resources.py 文件中的 UpdateUserInfoResource 对象
        # endpoint 不填写时默认为空，映射为根路由
        ResourceRoute("POST", resource.app0.update_user_info, endpoint="info"),
        # 我们也可以使用常规的方式进行声明，但不推荐
        ResourceRoute("POST", UpdateUserInfoResource),
        # 如果我们涉及到了 RestFul 标准的更新、删除类型，则可以使用 pk_field 声明，会自动将 pk 添加到 validated_request_data 中
        ResourceRoute("PUT", UpdateUserInfoResource, pk_field="user_id"),
    ]
```

## ResourceRoute

目前，ResourceRoute支持以下属性配置：

- `method`: 请求方法，目前支持GET, POST, PUT, PATCH, DELETE
- `resource_class`: 需要调用的Resource类
- `endpoint`: 定义追加的url后缀，如在`TestViewSet`中定义了一个`endpoint`为`my_endpoint`的`ResourceRoute`，则访问链接为`.../test/my_endpoint/`
  ，若不定义`endpoint`，则为`.../test/`
- `enable_paginate`: 是否启动分页功能，当对应的`Resource`配置了`many_response_data = True`才有效

