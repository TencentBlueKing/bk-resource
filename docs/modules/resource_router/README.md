> ResourceRouter

## ResourceRouter 使用

基于 `rest_framework.routers.DefaultRouter` 扩展的Router。

与 DefaultRouter 相比，增加了导入整个 views 模块的函数 `register_module`，通过自动扫描 ViewSet 类，并根据 ViewSet 名称动态增加 url，免去逐个为 ViewSet 定义 url 的麻烦。

```python
from bk_resource.routers import ResourceRouter
from example.app0 import views

router = ResourceRouter()
router.register_module(views)

urlpatterns = router.urls
```
