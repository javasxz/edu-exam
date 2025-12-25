from common.routers import DefaultRouter
from .views import *


router = DefaultRouter()
router.register("token", TokenViewSet, basename="token")
