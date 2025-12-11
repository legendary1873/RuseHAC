"""Admin for resources app."""

from django.contrib import admin
from .models import Resource, Submission, SubmissionFeedback


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "uploaded_by", "approved", "created_at")
    list_filter = ("approved", "category", "created_at")
    search_fields = ("title", "uploaded_by__email", "tags")


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "submitted_at")
    list_filter = ("submitted_at",)
    search_fields = ("title", "user__email")


@admin.register(SubmissionFeedback)
class SubmissionFeedbackAdmin(admin.ModelAdmin):
    list_display = ("submission", "given_by", "created_at")
    list_filter = ("created_at",)
    search_fields = ("submission__title", "given_by__email")
