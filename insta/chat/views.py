from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Message,Notificaton
from django.contrib.auth.models import User
from django.db.models import Count 
from django.db.models import Q
from django.utils import timezone
from datetime import date


@login_required
def main_chat(request, user_id):
    user_obj = User.objects.get(id=user_id)
    users = User.objects.exclude(id=request.user.id)
    
    
    # Determine the receiver based on user_id
    receiver = User.objects.get(id=user_id)

    if request.user.id > user_obj.id:
        thread_name = f'chat_{request.user.id}-{user_obj.id}'
    else:
        thread_name = f'chat_{user_obj.id}-{request.user.id}'

    messages = Message.objects.filter(theard_name=thread_name)
    last_seen = (
        Message.objects.filter(user=user_obj)
        .order_by('-date')
        .values_list('date', flat=True)
        .first()
)    

 # Fetch notifications related to the messages for the current user and mark them as seen
    notifications = Notificaton.objects.filter(message__in=messages, receiver=request.user, is_seen=False)
    
    # Mark notifications as seen
    notifications.update(is_seen=True) 
    messages.update(is_read=True)

    today = timezone.now().date()
    context = {
        'users': users,
        'user': user_obj,
        'messages': messages,
        'today': today,
        'last_seen': last_seen,
    }

    return render(request, 'message.html', context)


# def chat(request):
#     user = request.user

#     # Get latest message per conversation pair
#     messages = Message.objects.filter(
#         Q(user=user) | Q(receiver=user)
#     ).order_by('-date')

#     latest_messages = {}
#     for message in messages:
#         other_user = message.receiver if message.user == user else message.user
#         if other_user not in latest_messages:
#             latest_messages[other_user] = message  # first one is latest due to ordering

#     notification_counts_receiver = (
#         Notificaton.objects.filter(
#             receiver=user,
#             is_seen=False
#         )
#         .values('user')  
#         .annotate(count=Count('id'))
#     )
#     print(latest_messages)
#     context = {
#         'users': list(latest_messages.values()),
#         'notification_counts_receiver': notification_counts_receiver,
#     }

#     return render(request, 'new_chat.html', context)




from django.db.models import OuterRef, Subquery, Count, Q

def chat(request):
    user = request.user

    # Subquery: latest message id between current user and each other user
    latest_msg_subquery = Message.objects.filter(
        Q(user=user, receiver=OuterRef('pk')) | Q(user=OuterRef('pk'), receiver=user)
    ).order_by('-date')

    # Users who have chatted with current user
    chat_users = User.objects.exclude(id=user.id).filter(
        Q(sent_messages__receiver=user) | Q(received_messages__user=user)
    ).distinct().annotate(
        latest_message_id=Subquery(latest_msg_subquery.values('id')[:1])
    )

    # Fetch all latest messages for chat users in one go
    latest_message_ids = [u.latest_message_id for u in chat_users if u.latest_message_id]
    latest_messages = Message.objects.filter(id__in=latest_message_ids).order_by('-date')

    # Build a dict for quick lookup of latest messages by id
    latest_messages_dict = {msg.id: msg for msg in latest_messages}

    print(latest_messages_dict,'dict')

    # Attach latest message object to each chat_user
    for chat_user in chat_users:
        chat_user.latest_msg = latest_messages_dict.get(chat_user.latest_message_id, None)

    # Notifications count grouped by sender user
    notification_counts_receiver = (
        Notificaton.objects.filter(
            receiver=user,
            is_seen=False
        )
        .values('user')
        .annotate(count=Count('id'))
    )
    

    context = {
        'chat_users': chat_users,
        'notification_counts_receiver': notification_counts_receiver,
    }

    return render(request, 'new_chat.html', context)
























# def chat(request):
#     user = request.user

#     # Get all messages where the current user is either the sender or receiver
#     all_messages_sent = Message.objects.filter(user=user).order_by('-date')
#     all_messages_received = Message.objects.filter(receiver=user).order_by('-date')

#     # Combine sent and received messages into a single queryset
#     all_messages = all_messages_sent | all_messages_received

#     # Create a dictionary to store the latest message for each user
#     latest_messages = {}

#     # Create a dictionary to store the count of unread messages for each user
#     unread_counts = {}

#     # Iterate through messages and keep track of the latest message and unread count for each user
#     for message in all_messages:

#         if message.user == user:
#             other_user = message.receiver
#         else:
#             other_user = message.user

#         # Check if Other User Exists in latest_messages or if the Message is More Recent
#         if other_user not in latest_messages or message.date > latest_messages[other_user].date:
#         # Update latest_messages with the Current Message
#             latest_messages[other_user] = message

#         # Count unread messages
#             unread_count = Message.objects.filter(receiver=user, user=other_user, is_read=False).count()
#             unread_counts[other_user] = unread_count

#     # Get message counts for all users
#     message_counts = Message.objects.filter(user=user).values('receiver').annotate(count=Count('receiver'))x    

#     # Convert the dictionary values to a list to pass to the template
#     unique_users = list(latest_messages.values())

#     context = {
#         'users': unique_users,
#         'unread_counts': unread_counts,  # Add unread_counts to the context
#     }
#     return render(request, 'chat.html', context)

