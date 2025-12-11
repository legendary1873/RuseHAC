"""Admin configuration for accounts app."""

from django.contrib import admin
from .models import CustomUser, ExecApplication


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
        "year_group",
        "role",
        "is_banned",
    )
    list_filter = ("role", "year_group", "is_banned")
    search_fields = ("email", "first_name", "last_name")
    fieldsets = (
        ("Personal Info", {"fields": ("email", "first_name", "last_name")}),
        ("Club Info", {"fields": ("year_group", "role", "bio")}),
        ("Ban Status", {"fields": ("is_banned", "ban_reason", "ban_until")}),
        ("Preferences", {"fields": ("email_notifications",)}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )


@admin.register(ExecApplication)
class ExecApplicationAdmin(admin.ModelAdmin):
    list_display = ("user", "status", "applied_at")
    list_filter = ("status", "applied_at")
    search_fields = ("user__email", "user__first_name", "user__last_name")
