"""URLs for core app."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"announcements", views.AnnouncementViewSet, basename="announcement")
router.register(r"meetings", views.MeetingViewSet, basename="meeting")
router.register(r"attendance", views.AttendanceViewSet, basename="attendance")

urlpatterns = [
    path("", include(router.urls)),
]
