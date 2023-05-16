# -*- coding: utf-8 -*-

from django.urls import include, path

urlpatterns = (
    path("", include("modules.default.entry.urls")),
    path("", include("modules.default.example.urls")),
)
