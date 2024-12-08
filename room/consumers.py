from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from .models import Room, Message, RoomUser

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.username = self.scope['url_route']['kwargs']['username']
        self.room_group_name = f'room_{self.room_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Add user to room
        await self.add_user_to_room(self.room_id, self.username)

        # Notify room of new user
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_list',
                'action': 'add',
                'username': self.username
            }
        )

        # Accept WebSocket connection
        await self.accept()

    async def disconnect(self, code):
        # Remove user from room
        await self.remove_user_from_room(self.room_id, self.username)

        # Notify room of user leaving
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_list',
                'action': 'remove',
                'username': self.username
            }
        )

        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message", "")
        sender = data.get("sender", "")

        # Save the message to the database
        await self.create_message(message, sender)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))

    async def user_list(self, event):
        action = event['action']
        username = event['username']

        # Retrieve current user list from the room group
        user_list = await self.get_user_list(self.room_id)

        # Send updated user list to WebSocket
        await self.send(text_data=json.dumps({
            'action': action,
            'username': username,
            'users': user_list
        }))

    @database_sync_to_async
    def create_message(self, message, sender):
        room = Room.objects.get(room_id=self.room_id)
        Message.objects.create(room=room, message=message, sender=sender)

    @database_sync_to_async
    def add_user_to_room(self, room_id, username):
        room = Room.objects.get(room_id=room_id)
        RoomUser.objects.get_or_create(room=room, username=username)

    @database_sync_to_async
    def remove_user_from_room(self, room_id, username):
        room = Room.objects.get(room_id=room_id)
        RoomUser.objects.filter(room=room, username=username).delete()

    @database_sync_to_async
    def get_user_list(self, room_id):
        room = Room.objects.get(room_id=room_id)
        return list(RoomUser.objects.filter(room=room).values_list('username', flat=True))
