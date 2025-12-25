from common.routers import DefaultRouter

from .views import *


router = DefaultRouter()
router.register("auth/token", TokenViewSet, basename="auth-token")
router.register("users", UserViewSet, basename="users")
