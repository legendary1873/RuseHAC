"""Models for notifications app."""

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Notification(models.Model):
    """A notification for a user."""

    class Type(models.TextChoices):
        ANNOUNCEMENT = "announcement", "Announcement"
        BALLOT = "ballot", "Ballot"
        MESSAGE = "message", "Message"
        SYSTEM = "system", "System"

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications"
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    notification_type = models.CharField(
        max_length=50, choices=Type.choices, default=Type.SYSTEM
    )
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    email_sent = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
