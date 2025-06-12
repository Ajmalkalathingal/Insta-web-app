from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async 
from .models import Message,Notificaton  
from django.contrib.auth.models import User
import base64
from django.core.files.base import ContentFile


class MyAsyncWebsocketConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.my_id = self.scope['user'].id
        self.other_user_id = self.scope['url_route']['kwargs']['id']

        if int(self.my_id) > int(self.other_user_id):
            self.room_name = f'{self.my_id}-{self.other_user_id}'
        else:
            self.room_name = f'{self.other_user_id}-{self.my_id}'

        self.group_room_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(self.group_room_name, self.channel_name)
        await self.accept()
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'You are now connected!'
        }))


    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)

        user_name = data['username']
        receiver = data['receiver']
        message_type = data.get('message_type', 'text')
        image_data = data.get('image', '')

        if message_type == 'text':
            message = data.get('message', '')
            await self.chatMessageSave(user_name, self.group_room_name, message, receiver, message_type)
        elif message_type == 'image':
            await self.chatMessageSave(user_name, self.group_room_name, image_data, receiver, message_type)

        await self.channel_layer.group_send(
            self.group_room_name,
            {
                'type': 'chat_message',
                'message': data.get('message', ''),  # Include message in case of text for consistency
                'username': user_name,
                'receiver': receiver,
                'message_type': message_type,
                'image': image_data
            }
        )

    async def chat_message(self, event):
        await self.send(json.dumps({
            'message': event['message'],
            'username': event['username'],
            'receiver': event['receiver'],
            'message_type': event['message_type'],
            'image': event.get('image', '')
        }))

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_room_name, self.channel_name)

    @database_sync_to_async
    def chatMessageSave(self, username, thread_name, content, receiver_username, message_type):
        sender_user = User.objects.get(username=username)
        receiver_user = User.objects.get(username=receiver_username)

        if message_type == 'text':
            msg_instance = Message.objects.create(
                user=sender_user, receiver=receiver_user, message=content, theard_name=thread_name)
        elif message_type == 'image':
            try:
                format, imgstr = content.split(';base64,')
                ext = format.split('/')[-1]
                image = ContentFile(base64.b64decode(imgstr), name=f'{thread_name}_{receiver_user.id}.{ext}')
                msg_instance = Message.objects.create(
                    user=sender_user, receiver=receiver_user, image=image, theard_name=thread_name)
            except ValueError:
                print("Error: message is not in the correct base64 format")
                return

        Notificaton.objects.create(
            user=sender_user, receiver=receiver_user, message=msg_instance)





class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['user'].id
        self.room_group_name = f'{self.user_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Get the initial notification count and send it to the client
        initial_notification_count, user_id, receiver_id = await self.notification_count()
        
        # Send the initial notification count to the client
        await self.send_notification({
            'count': initial_notification_count,
            'user': receiver_id,
            'user_receiver': user_id
        })

    async def send_notification(self, event):
        # print(event)
        await self.send(json.dumps(event))

    async def send_notifications(self, event):
        data = event.get('value')  # Fetch data

        if data:
            data_dict = json.loads(data)
            notification_message_count = data_dict.get('count')
            receiver = data_dict.get('receiver')
            user = data_dict.get('user')

            # Check if all necessary data is available before sending the notification
            if  receiver is not None and user is not None:
                await self.send(json.dumps({
                    "count": notification_message_count,
                    'user': user,
                    'user_receiver': receiver
                }))
            else:
                print("Incomplete data received in send_notifications.")
        else:
            print("No data received in send_notifications.")

    @database_sync_to_async
    def notification_count(self):
        try:
            user = User.objects.get(id=self.user_id)
        except User.DoesNotExist:
            return 0, self.user_id, self.user_id  # fallback if user not found

        # Get unseen notifications where current user is the receiver
        notifications = Notificaton.objects.select_related('message__user').filter(
            message__receiver=user,
            is_seen=False
        )

        if notifications.exists():
            latest_notification = notifications.order_by('-id').first()
            sender = latest_notification.message.user

            notification_count = notifications.filter(
                message__user=sender
            ).count()

            return notification_count, sender.id, user.id
        else:
            # No unseen notifications: just return 0 and the user ID as receiver
            return 0, None, user.id


