from bk_resource.routers import ResourceRouter
from tests.mock import views

router = ResourceRouter()
router.register_module(views)

urlpatterns = router.urls
