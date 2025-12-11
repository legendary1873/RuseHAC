"""Admin configuration for core app."""

from django.contrib import admin
from .models import Announcement, Meeting, Attendance


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "pinned", "created_at")
    list_filter = ("pinned", "created_at")
    search_fields = ("title", "content", "author__email")


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "created_by")
    list_filter = ("date",)
    search_fields = ("title", "created_by__email")


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("user", "meeting", "marked_at")
    list_filter = ("marked_at", "meeting__date")
    search_fields = ("user__email", "meeting__title")
