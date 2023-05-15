# -*- coding: utf-8 -*-

from bk_resource import resource
from bk_resource.viewsets import ResourceRoute, ResourceViewSet


class ExampleViewSet(ResourceViewSet):
    resource_routes = [
        ResourceRoute("GET", resource.example.user_info),
    ]
