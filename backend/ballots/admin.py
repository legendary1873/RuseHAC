"""Admin for ballots app."""

from django.contrib import admin
from .models import Ballot, BallotOption, Vote


@admin.register(Ballot)
class BallotAdmin(admin.ModelAdmin):
    list_display = ("title", "created_by", "closing_date", "closed")
    list_filter = ("closed", "created_at")
    search_fields = ("title", "created_by__email")


@admin.register(BallotOption)
class BallotOptionAdmin(admin.ModelAdmin):
    list_display = ("text", "ballot", "vote_count")
    search_fields = ("text", "ballot__title")


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("user", "ballot", "option", "created_at")
    list_filter = ("created_at", "ballot")
    search_fields = ("user__email", "ballot__title")
