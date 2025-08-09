import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatRoom, Message
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # room name from URL route
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.group_name = f'chat_{self.room_name}'

        # Accept connection
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        # Optionally: send a system message about join (not persistent)
        # await self.send_json({"system": f"Joined {self.room_name}"})

    async def disconnect(self, close_code):
        # Leave group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        """
        Called when a message is received from the WebSocket.
        Expected JSON: { "message": "hello world" }
        """
        data = json.loads(text_data)
        message_text = data.get('message')

        # Determine user if authenticated; scope['user'] available when using AuthMiddlewareStack
        user = self.scope.get('user')
        username = None
        user_obj = None
        if user and user.is_authenticated:
            username = user.username
            user_obj = user

        # Save message to DB (sync DB operations wrapped)
        await self.save_message(self.room_name, user_obj, message_text)

        # Broadcast to room group
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat.message',            # name of handler below
                'message': message_text,
                'username': username,
            }
        )

    async def chat_message(self, event):
        # Handler for messages sent to the group
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event.get('username')
        }))

    @database_sync_to_async
    def save_message(self, room_name, user, message):
        room, _ = ChatRoom.objects.get_or_create(name=room_name)
        Message.objects.create(room=room, user=user, content=message)
