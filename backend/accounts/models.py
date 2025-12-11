"""Models for user accounts."""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import URLValidator
import hashlib


class CustomUser(AbstractUser):
    """Extended user model with club-specific fields."""

    class YearGroup(models.TextChoices):
        YEAR_7 = "Y7", "Year 7"
        YEAR_8 = "Y8", "Year 8"
        YEAR_9 = "Y9", "Year 9"
        YEAR_10 = "Y10", "Year 10"
        YEAR_11 = "Y11", "Year 11"
        YEAR_12 = "Y12", "Year 12"
        YEAR_13 = "Y13", "Year 13"

    class Role(models.TextChoices):
        MEMBER = "member", "Member"
        EXEC = "exec", "Executive"
        ADMIN = "admin", "Admin"

    email = models.EmailField(unique=True)
    year_group = models.CharField(max_length=3, choices=YearGroup.choices)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.MEMBER)
    bio = models.TextField(blank=True, default="")
    is_banned = models.BooleanField(default=False)
    ban_reason = models.TextField(blank=True, default="")
    ban_until = models.DateTimeField(null=True, blank=True)
    email_notifications = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_gravatar_url(self):
        """Get Gravatar URL based on email."""
        email_hash = hashlib.md5(self.email.lower().encode()).hexdigest()
        return f"https://www.gravatar.com/avatar/{email_hash}?d=identicon"

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.email


class ExecApplication(models.Model):
    """Application for executive position."""

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="exec_application"
    )
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.PENDING
    )
    statement = models.TextField()
    applied_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_applications",
    )

    class Meta:
        ordering = ["-applied_at"]

    def __str__(self):
        return f"{self.user.email} - {self.status}"
