"""Serializers for core app."""

from rest_framework import serializers
from .models import Announcement, Meeting, Attendance


class AnnouncementSerializer(serializers.ModelSerializer):
    author_email = serializers.CharField(source="author.email", read_only=True)

    class Meta:
        model = Announcement
        fields = (
            "id",
            "title",
            "content",
            "author",
            "author_email",
            "created_at",
            "pinned",
        )
        read_only_fields = ("id", "author", "author_email", "created_at")


class MeetingSerializer(serializers.ModelSerializer):
    created_by_email = serializers.CharField(source="created_by.email", read_only=True)
    attendance_count = serializers.SerializerMethodField()

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
        )
        read_only_fields = ("id", "created_by", "created_at")

    def get_attendance_count(self, obj):
        return obj.attendances.count()


class AttendanceSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source="user.email", read_only=True)
    meeting_title = serializers.CharField(source="meeting.title", read_only=True)

    class Meta:
        model = Attendance
        fields = (
            "id",
            "user",
            "user_email",
            "meeting",
            "meeting_title",
            "marked_at",
            "marked_by",
        )
        read_only_fields = ("id", "marked_at", "marked_by")
