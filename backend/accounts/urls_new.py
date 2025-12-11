"""URL configuration for accounts app."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views_new import CustomTokenObtainPairView, UserViewSet, ExecApplicationViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(
    r"exec-applications", ExecApplicationViewSet, basename="exec-application"
)

urlpatterns = [
    path("", include(router.urls)),
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
