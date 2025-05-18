from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async 
from .models import Message,Notificaton,ChatGroup  
from django.contrib.auth.models import User
import base64
from django.core.files.base import ContentFile


# class MyAsyncWebsocketConsumer(AsyncWebsocketConsumer):

#     async def connect(self):
#         self.my_id = self.scope['user'].id
#         self.other_user_id = self.scope['url_route']['kwargs']['id']

#         if int(self.my_id) > int(self.other_user_id):
#             self.room_name = f'{self.my_id}-{self.other_user_id}'
#         else:
#             self.room_name = f'{self.other_user_id}-{self.my_id}'

#         self.group_room_name = f'chat_{self.room_name}'

#         await self.channel_layer.group_add(self.group_room_name, self.channel_name)
#         await self.accept()
#         await self.send(text_data=json.dumps({
#             'type': 'connection_established',
#             'message': 'You are now connected!'
#         }))


#     async def receive(self, text_data=None, bytes_data=None):
#         data = json.loads(text_data)

#         user_name = data['username']
#         receiver = data['receiver']
#         message_type = data.get('message_type', 'text')
#         image_data = data.get('image', '')

#         if message_type == 'text':
#             message = data.get('message', '')
#             await self.chatMessageSave(user_name, self.group_room_name, message, receiver, message_type)
#         elif message_type == 'image':
#             await self.chatMessageSave(user_name, self.group_room_name, image_data, receiver, message_type)

#         await self.channel_layer.group_send(
#             self.group_room_name,
#             {
#                 'type': 'chat_message',
#                 'message': data.get('message', ''),  # Include message in case of text for consistency
#                 'username': user_name,
#                 'receiver': receiver,
#                 'message_type': message_type,
#                 'image': image_data
#             }
#         )

#     async def chat_message(self, event):
#         await self.send(json.dumps({
#             'message': event['message'],
#             'username': event['username'],
#             'receiver': event['receiver'],
#             'message_type': event['message_type'],
#             'image': event.get('image', '')
#         }))

#     async def disconnect(self, code):
#         await self.channel_layer.group_discard(self.group_room_name, self.channel_name)

#     @database_sync_to_async
#     def chatMessageSave(self, username, thread_name, content, receiver_username, message_type):
#         sender_user = User.objects.get(username=username)
#         receiver_user = User.objects.get(username=receiver_username)

#         if message_type == 'text':
#             msg_instance = Message.objects.create(
#                 user=sender_user, receiver=receiver_user, message=content, theard_name=thread_name)
#         elif message_type == 'image':
#             try:
#                 format, imgstr = content.split(';base64,')
#                 ext = format.split('/')[-1]
#                 image = ContentFile(base64.b64decode(imgstr), name=f'{thread_name}_{receiver_user.id}.{ext}')
#                 msg_instance = Message.objects.create(
#                     user=sender_user, receiver=receiver_user, image=image, theard_name=thread_name)
#             except ValueError:
#                 print("Error: message is not in the correct base64 format")
#                 return

#         Notificaton.objects.create(
#             user=sender_user, receiver=receiver_user, message=msg_instance)




class MyAsyncWebsocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        
        self.chat_type = self.scope['url_route']['kwargs'].get('chat_type')
        self.my_id = self.scope['user'].id

        if self.chat_type == 'private':
            self.other_user_id = self.scope['url_route']['kwargs']['id']
            if int(self.my_id) > int(self.other_user_id):
                self.room_name = f'{self.my_id}-{self.other_user_id}'
            else:
                self.room_name = f'{self.other_user_id}-{self.my_id}'
            self.thread_name = f'private_{self.room_name}'
        else:  # group chat
            self.group_name = self.scope['url_route']['kwargs']['group_name']
            self.thread_name = self.group_name

        self.room_group_name = self.thread_name

        print(f"[CONNECT] User {self.my_id} joined room: {self.room_group_name}")

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        
        data = json.loads(text_data)

        username = data.get('username')
        message_type = data.get('message_type', 'text')
        message = data.get('message', '')
        image_data = data.get('image', '')

        receiver = None  # default


        if self.chat_type == 'group':
            group_name = data.get('group_name')
            await self.save_group_message(
                sender_username=username,
                group_name=group_name,
                content=message,
                message_type=message_type,
                image_data=image_data,
                thread_name=self.thread_name
            )
        else:
            receiver = data.get('receiver')
            await self.save_private_message(
                sender_username=username,
                receiver=receiver,
                content=message,
                message_type=message_type,
                image_data=image_data,
                thread_name=self.thread_name
            )

        print(f"[RECEIVE] From {username} to {receiver} → {message}")
        
        # Send message to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'username': username,
                'receiver': receiver,  # None for group
                'message': message,
                'message_type': message_type,
                'image': image_data
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'username': event['username'],
            'receiver': event.get('receiver'),  # safe access
            'message': event['message'],
            'message_type': event['message_type'],
            'image': event['image']
        }))
        print(f"[SEND] Delivering: {event}")

    @database_sync_to_async
    def save_private_message(self, sender_username, receiver, content, message_type, image_data, thread_name):
        try:
            sender = User.objects.get(username=sender_username)
            receiver = User.objects.get(username=receiver)

            if message_type == 'text':
                msg_instance = Message.objects.create(
                    user=sender,
                    receiver=receiver,
                    theard_name=thread_name,
                    message=content
                )
            elif message_type == 'image':
                format, imgstr = image_data.split(';base64,')
                ext = format.split('/')[-1]
                image = ContentFile(base64.b64decode(imgstr), name=f'{sender.username}_{receiver.username}.{ext}')
                msg_instance = Message.objects.create(
                    user=sender,
                    receiver=receiver,
                    theard_name=thread_name,
                    image=image
                )

            Notificaton.objects.create(user=sender, receiver=receiver, message=msg_instance)
        except User.DoesNotExist:
            print(f"[Private] User not found: {sender_username} or {receiver_username}")

    @database_sync_to_async
    def save_group_message(self, sender_username, group_name, content, message_type, image_data, thread_name):
        try:
            sender = User.objects.get(username=sender_username)
            group = ChatGroup.objects.get(name=group_name)

            if message_type == 'text':
                msg_instance = Message.objects.create(
                    user=sender,
                    group=group,
                    message=content,
                    theard_name=thread_name
                )
            elif message_type == 'image':
                format, imgstr = image_data.split(';base64,')
                ext = format.split('/')[-1]
                image = ContentFile(base64.b64decode(imgstr), name=f'{group_name}_{sender.username}.{ext}')
                msg_instance = Message.objects.create(
                    user=sender,
                    group=group,
                    image=image,
                    theard_name=thread_name
                )

            for member in group.members.exclude(id=sender.id):
                Notificaton.objects.create(user=sender, receiver=member, message=msg_instance)
        except (User.DoesNotExist, ChatGroup.DoesNotExist) as e:
            print(f"[Group] Error saving group message: {e}")




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
            'type': 'notification_countt',
            'count': initial_notification_count,
            'user': receiver_id,
            'user_receiver': user_id
        })

    async def send_notification(self, event):
        # print(event)
        await self.send(json.dumps(event))

    async def send_notifications(self, event):
        data = event.get('value')  # Fetch data

        # print(data, 'data')

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
        # Handle the case where the user doesn't exist
            return 0, self.user_id, self.user_id

        notifications = Notificaton.objects.select_related('message__user').filter(message__receiver=user, is_seen=False)
        notification_count = notifications.count()

        user_id = self.user_id
        receiver_id = None

        if notification_count > 0:
            first_notification = notifications.first()
            receiver = first_notification.message.user
            receiver_id = receiver.id
        else:
            # Try to fetch the most recent message and extract the sender (as fallback receiver)
            latest_message = Message.objects.filter(receiver=user).order_by('-date').first()
            if latest_message:
                receiver_id = latest_message.user.id
            else:
                # Default to self for edge case fallback
                receiver_id = user_id

        return notification_count, user_id, receiver_id



    async def disconnect(self, event):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
