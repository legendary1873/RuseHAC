"""Admin for notifications app."""

from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "title",
        "notification_type",
        "read",
        "email_sent",
        "created_at",
    )
    list_filter = ("read", "email_sent", "notification_type", "created_at")
    search_fields = ("user__email", "title", "content")
