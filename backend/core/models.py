"""Models for core app - attendance and club data."""

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Announcement(models.Model):
    """Club announcements created by execs."""

    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="announcements"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    pinned = models.BooleanField(default=False)

    class Meta:
        ordering = ["-pinned", "-created_at"]

    def __str__(self):
        return self.title


class Meeting(models.Model):
    """Club meeting for attendance tracking."""

    title = models.CharField(max_length=255)
    date = models.DateTimeField()
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_meetings"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f'{self.title} - {self.date.strftime("%Y-%m-%d")}'


class Attendance(models.Model):
    """Record of user attendance at meetings."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="attendance_records"
    )
    meeting = models.ForeignKey(
        Meeting, on_delete=models.CASCADE, related_name="attendances"
    )
    marked_at = models.DateTimeField(auto_now_add=True)
    marked_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="marked_attendance"
    )

    class Meta:
        unique_together = ("user", "meeting")

    def __str__(self):
        return f"{self.user.email} - {self.meeting.title}"
