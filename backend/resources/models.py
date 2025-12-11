"""Models for resources app - shared materials and submissions."""

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Resource(models.Model):
    """Shared educational resource."""

    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to="resources/")
    category = models.CharField(max_length=100)
    tags = models.CharField(max_length=255, blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_resources",
    )


class Submission(models.Model):
    """User essay/assignment submission for feedback."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submissions")
    title = models.CharField(max_length=255)
    content = models.TextField()
    file = models.FileField(upload_to="submissions/")
    submitted_at = models.DateTimeField(auto_now_add=True)


class SubmissionFeedback(models.Model):
    """Feedback on a submission."""

    submission = models.ForeignKey(
        Submission, on_delete=models.CASCADE, related_name="feedback"
    )
    given_by = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
