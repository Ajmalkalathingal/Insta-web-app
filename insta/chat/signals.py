from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notificaton,Message
from django.db.models import Count 

import json

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# @receiver(post_save, sender=Notificaton)
# def get_notification(sender, instance, created, **kwargs):
#     if created:
#         channel_layer = get_channel_layer()
#         receiver_user = instance.message.receiver
#         notification_count = Notificaton.objects.filter(message__receiver=receiver_user, is_seen=False).count()
        
#         room_name = str(receiver_user.id)

#         data = {
#             'count': notification_count,
#             'user': receiver_user.id
#         }

#         async_to_sync(channel_layer.group_send)(
#             room_name, {
#                 'type': 'send_notifications',
#                 'value': json.dumps(data)
#             }
#         )

@receiver(post_save, sender=Notificaton)
def get_notification(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        receiver_user = instance.message.receiver
        user = instance.message.user

        # Calculate notification count for the specific receiver user
        notification_count = Notificaton.objects.filter(
            message__receiver=receiver_user,
            user=user,
            is_seen=False
        ).count()

        # print(notification_count, 'notification_count for user',receiver_user)
        # Prepare data for WebSocket message
        data = {
            'count': notification_count,
            'receiver': receiver_user.id,
            'user' : user.id
        }
        print(data)
        # Send WebSocket message to the specific user
        room_name = str(receiver_user.id)
        # print('room name notification',room_name)
        async_to_sync(channel_layer.group_send)(
            room_name, {
                'type': 'send_notifications',
                'value': json.dumps(data)
            }
        )