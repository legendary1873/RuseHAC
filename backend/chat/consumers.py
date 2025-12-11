"""Consumers for WebSocket chat."""

from channels.generic.websocket import AsyncWebsocketConsumer
import json


class ChatConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for chat messages."""

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message")

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat.message",
                "message": message,
                "user": self.scope["user"].email,
            },
        )

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps({"message": event["message"], "user": event["user"]})
        )


class NotificationConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for notifications."""

    async def connect(self):
        self.user_id = self.scope["url_route"]["kwargs"]["user_id"]
        self.user_group_name = f"notifications_{self.user_id}"

        await self.channel_layer.group_add(self.user_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.user_group_name, self.channel_name)

    async def notification(self, event):
        await self.send(text_data=json.dumps({"notification": event["notification"]}))
