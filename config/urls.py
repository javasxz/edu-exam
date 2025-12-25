"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from common.routers import DefaultRouter
from my_auth.urls import router as auth_router
from users.urls import router as users_router
from exams.urls import router as exams_router


router_v1 = DefaultRouter()
router_v1.register_nested("auth", auth_router)
router_v1.extend(users_router)
router_v1.extend(exams_router)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router_v1.urls)),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"),name="swagger-ui")
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

