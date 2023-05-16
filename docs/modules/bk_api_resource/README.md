> BKAPIResource

# APIResource
APIResource将一个API接口封装为Resource，便于调用
```python
class APIResource(ApiResourceProtocol, CacheResource, metaclass=abc.ABCMeta)
```
**主要方法和属性：**

`module`：模块名，主要用于调试

`TIMEOUT`请求超时时间

`url_keys`用于path参数的映射

`def request(self, request_data=None, **kwargs):`

调用父类`Resource`请求流程(校验请求参数-处理逻辑-验证返回数据)

`def perform_request(self, validated_request_data):`

发起http请求，可以识别非GET请求中的文件数据。
1. `def build_request_data(self, validated_request_data):`

   请求前对请求参数做处理
2. `def build_url(self, validated_request_data):`

   拼接最终URL
3. `def build_header(self, validated_request_data):`

   在请求前构造请求头
4. `def before_request(self, kwargs):`

   对于非GET请求，如果不存在文件数据则按照JSON方式请求，否则分开传参，可以由此方啊做最后的处理。
5. `def parse_response(self, response: requests.Response):`

   在提供数据给`response_serializer`之前，对数据作最后的处理。尝试解析json数据，返回数据的`data`部分。
# BkApiResource
`class BkApiResource(APIResource, abc.ABC):`

基于`APiResource`在请求时携带鉴权信息，并对返回数据做鉴权认证。
1. `method = "GET"`：请求方法默认为GET
2. `bkapi_header_authorization`：api头部鉴权
3. `platform_authorization`：平台鉴权

**样例：**

定义API
```python
# api/bk_community/default.py

import abc

from bk_resource import BkApiResource
from django.utils.translation import gettext_lazy


class CommunityResource(BkApiResource, abc.ABC):
   base_url = "https://bk.tencent.com/s-mart/forum"
   module_name = "bk_community"


class TopicsResource(CommunityResource):
   name = gettext_lazy("查询论坛主题")
   method = "GET"
   action = "/topics/"
```
调用API：
```python
from bk_resource import api

api.bk_community.topics(keyword="test", page=1, page_size=1)
```
实际请求`url`为`https://bk.tencent.com/s-mart/forum/topics/?page=1&page_size=10&keyword=test`

**path参数**

如果接口中存在path参数则可以按照以下方式进行编写
```python
class TopicsResource(CommunityResource):
    name = gettext_lazy("查询模块")
    method = "GET"
    action = "/forum/topics/{topic_id}"
    url_keys = ["topic_id"]
```
调用API：
```python
from bk_resource import api

api.bk_community.topics(keyword="test", topic_id=2002)
```
实际请求url为`https://bk.tencent.com/s-mart/forum/topics/1002/?keyword=test`

**其他**

因为`BkApiResource`继承于`Resource`，因此可以使用`Resource`相关功能，如可以重写`RequestSerializer`和`ResponseSerializer`属性对请求参数和返回数据进行校验和处理。