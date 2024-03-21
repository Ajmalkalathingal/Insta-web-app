from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async 
from .models import Message,Notificaton  
from django.contrib.auth.models import User
from django.db.models import Count 


class MyAsyncWebsocketConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        # print('websocket connected')
        self.my_id = self.scope['user'].id
        self.other_user_id = self.scope['url_route']['kwargs']['id']

        if int(self.my_id) > int(self.other_user_id):
            self.room_name = f'{self.my_id}-{self.other_user_id}'
        else:
            self.room_name = f'{self.other_user_id}-{self.my_id}'

        self.group_room_name = f'chat_{self.room_name}' 

        await self.channel_layer.group_add(self.group_room_name,self.channel_name)

        await self.accept() 
        await self.send(self.group_room_name)


    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data['message']
        user_name = data['username']
        receiver = data['receiver']
        # print('message', data)
        
        # save message
        await self.chatMessageSave(user_name,self.group_room_name,message,receiver) 

        await self.channel_layer.group_send(
            self.group_room_name,
            {
                'type': 'chat.message',
                'message': message,
                'username':user_name,
                'receiver':receiver
            }
        )

    async def chat_message(self, event):        
        await self.send(json.dumps({
            'message':event['message'],
            'username':event['username'],
            'receiver':event['receiver'],
        }))    

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.group_room_name, self.channel_name
        )
    
    @database_sync_to_async
    def chatMessageSave(self, username, thread_name, message, receiver_username):
        sender_user = User.objects.get(username=username)
        receiver_user = User.objects.get(username=receiver_username)

        message = Message.objects.create(user=sender_user, receiver=receiver_user, message=message, theard_name=thread_name)

        notification = Notificaton.objects.create(user=sender_user, receiver=receiver_user, message=message)




# class NotificationConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.user_id = self.scope['user'].id
#         self.room_group_name = f'{self.user_id}'
        
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()

#         # Get the initial notification count and send it to the client
#         initial_notification_count,user_id,receiver_id = await self.initial_notification_count()
        
 
#         await self.send_notification({
#             'type': 'initial_notification_count',
#             'count': initial_notification_count,
#             'user': user_id,
#             'receiver' : receiver_id
#         })

#     async def send_notification(self, event):
#         await self.send(json.dumps(event))


#     async def send_notifications(self, event):
#         data = event.get('value')  # Fetch data

#         if data:
#             data_dict = json.loads(data)
#             notification_message_count = data_dict['count']
#             receiver = data_dict['receiver']
#             user = data_dict['user']
#             # print(notification_message_count, "and user id", user)

#             await self.send(json.dumps({
#                 "count": notification_message_count,
#                 'user': user,
#                 'receiver': receiver
#             }))

#         else:
#             print("No data received in send_notifications.")
    
    
#     @database_sync_to_async
#     def initial_notification_count(self):
#         # Get the user based on the user_id
#         user = User.objects.get(id=self.user_id)

#         # Get notifications for the user
#         notifications = Notificaton.objects.filter(message__receiver=user, is_seen=False)

#         # Initialize notification count
#         notification_count = 0

#         # Initialize user_id and receiver_id to None
#         user_id = None
#         receiver_id = None

#         # Check if there are any notifications
#         if notifications.exists():
#             # If there are notifications, get the IDs
#             first_notification = notifications.first()
#             user = first_notification.message.user
#             user_id = user.id
#             receiver = first_notification.message.receiver
#             receiver_id = receiver.id

#             # Get the notification count
#             notification_count = notifications.count()

#         # Print the values for debugging
#         print(notification_count, 'initial count')
#         print(user_id, 'user_id')
#         print(receiver_id, 'receiver_id')

#         return notification_count, user_id, receiver_id




#     async def disconnect(self, event):
#          await self.channel_layer.group_discard(
#              self.room_group_name,
#              self.channel_name
#          )




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
        initial_notification_count, user_id, receiver_id = await self.initial_notification_count()
        
        # Send the initial notification count to the client
        await self.send_notification({
            'type': 'initial_notification_count',
            'count': initial_notification_count,
            # 'user': user_id,
            'user': receiver_id
        })

    async def send_notification(self, event):
        await self.send(json.dumps(event))

    async def send_notifications(self, event):
        data = event.get('value')  # Fetch data

        if data:
            data_dict = json.loads(data)
            notification_message_count = data_dict.get('count')
            receiver = data_dict.get('receiver')
            user = data_dict.get('user')

            # Check if all necessary data is available before sending the notification
            if notification_message_count is not None and receiver is not None and user is not None:
                await self.send(json.dumps({
                    "count": notification_message_count,
                    'user': user,
                    'receiver': receiver
                }))
            else:
                print("Incomplete data received in send_notifications.")
        else:
            print("No data received in send_notifications.")

    @database_sync_to_async
    def initial_notification_count(self):
        # Get the user based on the user_id
        user = User.objects.get(id=self.user_id)

        # Get notifications for the user
        notifications = Notificaton.objects.filter(message__receiver=user, is_seen=False)

        # Initialize notification count
        notification_count = notifications.count()

        # Initialize user_id and receiver_id
        user_id = self.user_id
        receiver_id =  None

        # Check if there are any notifications
        if notification_count > 0:
            # If there are notifications, get the IDs
            first_notification = notifications.first()
            receiver = first_notification.message.user
            receiver_id = receiver.id
        else:
            # If there are no notifications, check if there are any messages for the user
            latest_message = Message.objects.filter(receiver=user).order_by('-date').first()
            if latest_message:
                receiver_id = latest_message.user_id  # Use the sender's ID as the receiver ID
            else:
                # If there are no messages either, use the user's ID as the receiver ID
                receiver_id = self.user_id    

        # Print the values for debugging
        print(notification_count, 'initial count')
        print(user_id, 'user_id')
        print(receiver_id, 'receiver_id')

        return notification_count, user_id, receiver_id


    async def disconnect(self, event):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
