"""Serializers for ballots app."""

from rest_framework import serializers
from .models import Ballot, BallotOption, Vote


class BallotOptionSerializer(serializers.ModelSerializer):
    """Serializer for ballot options."""

    vote_count = serializers.SerializerMethodField()

    class Meta:
        model = BallotOption
        fields = ("id", "ballot", "text", "vote_count", "created_at")
        read_only_fields = ("id", "ballot", "created_at", "vote_count")

    def get_vote_count(self, obj):
        return obj.votes.count()


class BallotSerializer(serializers.ModelSerializer):
    """Serializer for ballots."""

    options = BallotOptionSerializer(many=True, read_only=True)
    created_by_email = serializers.CharField(source="created_by.email", read_only=True)
    user_vote = serializers.SerializerMethodField()
    is_open = serializers.SerializerMethodField()
    vote_count = serializers.SerializerMethodField()

    class Meta:
        model = Ballot
        fields = (
            "id",
            "title",
            "description",
            "created_by",
            "created_by_email",
            "created_at",
            "closing_date",
            "closed",
            "options",
            "user_vote",
            "is_open",
            "vote_count",
        )
        read_only_fields = ("id", "created_by", "created_at", "closed", "options")

    def get_user_vote(self, obj):
        """Get current user's vote on this ballot."""
        request = self.context.get("request")
        if request and request.user and request.user.is_authenticated:
            try:
                vote = Vote.objects.get(ballot=obj, user=request.user)
                return vote.option.id
            except Vote.DoesNotExist:
                return None
        return None

    def get_is_open(self, obj):
        """Check if ballot is open for voting."""
        from django.utils import timezone

        return not obj.closed and timezone.now() < obj.closing_date

    def get_vote_count(self, obj):
        """Total number of votes cast."""
        return obj.votes.count()


class VoteSerializer(serializers.ModelSerializer):
    """Serializer for casting votes."""

    ballot_title = serializers.CharField(source="ballot.title", read_only=True)
    option_text = serializers.CharField(source="option.text", read_only=True)
    user_email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Vote
        fields = (
            "id",
            "ballot",
            "ballot_title",
            "option",
            "option_text",
            "user",
            "user_email",
            "created_at",
        )
        read_only_fields = ("id", "user", "user_email", "created_at")
