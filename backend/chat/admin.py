"""Admin for chat app."""

from django.contrib import admin
from .models import ChatRoom, ChatMessage


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ("name", "is_private", "created_by", "created_at")
    list_filter = ("is_private", "created_at")
    search_fields = ("name", "created_by__email")


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("user", "room", "created_at", "deleted")
    list_filter = ("deleted", "created_at", "room")
    search_fields = ("user__email", "room__name", "content")
