"""Serializers for core app."""

from rest_framework import serializers
from django.utils import timezone
from .models import Announcement, Meeting, Attendance


class AnnouncementSerializer(serializers.ModelSerializer):
    """Serializer for announcements."""

    author_email = serializers.CharField(source="author.email", read_only=True)
    author_name = serializers.SerializerMethodField()

    class Meta:
        model = Announcement
        fields = (
            "id",
            "title",
            "content",
            "author",
            "author_email",
            "author_name",
            "created_at",
            "updated_at",
            "pinned",
        )
        read_only_fields = (
            "id",
            "author",
            "author_email",
            "author_name",
            "created_at",
            "updated_at",
        )

    def get_author_name(self, obj):
        return f"{obj.author.first_name} {obj.author.last_name}".strip()


class MeetingSerializer(serializers.ModelSerializer):
    """Serializer for meetings."""

    created_by_email = serializers.CharField(source="created_by.email", read_only=True)
    attendance_count = serializers.SerializerMethodField()
    is_past = serializers.SerializerMethodField()

    class Meta:
        model = Meeting
        fields = (
            "id",
            "title",
            "date",
            "description",
            "created_by",
            "created_by_email",
            "created_at",
            "attendance_count",
            "is_past",
        )
        read_only_fields = (
            "id",
            "created_by",
            "created_by_email",
            "created_at",
            "attendance_count",
            "is_past",
        )

    def get_attendance_count(self, obj):
        return obj.attendances.count()

    def get_is_past(self, obj):
        return obj.date < timezone.now()


class AttendanceSerializer(serializers.ModelSerializer):
    """Serializer for attendance records."""

    user_email = serializers.CharField(source="user.email", read_only=True)
    user_name = serializers.SerializerMethodField()
    meeting_title = serializers.CharField(source="meeting.title", read_only=True)

    class Meta:
        model = Attendance
        fields = (
            "id",
            "user",
            "user_email",
            "user_name",
            "meeting",
            "meeting_title",
            "marked_at",
            "marked_by",
        )
        read_only_fields = ("id", "marked_at", "marked_by")

    def get_user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip()


class AttendanceStatsSerializer(serializers.Serializer):
    """Serializer for attendance statistics."""

    attended = serializers.IntegerField()
    total = serializers.IntegerField()
    percentage = serializers.FloatField()
    target_percentage = serializers.IntegerField(default=70)
    on_target = serializers.BooleanField()
    remaining_needed = serializers.IntegerField()
