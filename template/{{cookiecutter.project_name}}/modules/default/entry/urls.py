# -*- coding: utf-8 -*-

from bk_resource.routers import ResourceRouter

from modules.default.entry import views

router = ResourceRouter()
router.register_module(views)

urlpatterns = router.urls
