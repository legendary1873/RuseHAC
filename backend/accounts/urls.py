"""URL configuration for accounts app."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ExecApplicationViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(
    r"exec-applications", ExecApplicationViewSet, basename="exec-application"
)

urlpatterns = [
    path("", include(router.urls)),
]
