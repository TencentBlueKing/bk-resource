from bk_resource import resource
from bk_resource.viewsets import ResourceRoute, ResourceViewSet


class MockViewSet(ResourceViewSet):
    resource_routes = [
        ResourceRoute("GET", resource.mock.test),
    ]
