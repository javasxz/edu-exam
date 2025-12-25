from common.routers import DefaultRouter

from .views import *


router = DefaultRouter()
router.register("exams", ExamViewSet, basename="exams")
