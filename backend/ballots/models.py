"""Models for ballots app - voting system."""

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Ballot(models.Model):
    """A voting ballot."""

    title = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    closing_date = models.DateTimeField()
    closed = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class BallotOption(models.Model):
    """Option in a ballot."""

    ballot = models.ForeignKey(Ballot, on_delete=models.CASCADE, related_name="options")
    text = models.CharField(max_length=255)
    vote_count = models.IntegerField(default=0)

    def __str__(self):
        return self.text


class Vote(models.Model):
    """A vote cast by a user."""

    ballot = models.ForeignKey(Ballot, on_delete=models.CASCADE, related_name="votes")
    option = models.ForeignKey(BallotOption, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("ballot", "user")

    def __str__(self):
        return f"{self.user.email} voted for {self.option.text}"
