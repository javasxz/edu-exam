from common.routers import DefaultRouter

from .views import *


router = DefaultRouter()
router.register("users", UserViewSet, basename="users")
