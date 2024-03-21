from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Message,Notificaton
from django.contrib.auth.models import User
from django.db.models import Count 
from django.http import JsonResponse


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
    

 # Fetch notifications related to the messages for the current user and mark them as seen
    notifications = Notificaton.objects.filter(message__in=messages, receiver=request.user, is_seen=False)
    
    # Mark notifications as seen
    notifications.update(is_seen=True) 


    context = {
        'users': users,
        'user': user_obj,
        'messages': messages,
    }

    return render(request, 'message.html', context)


def chat(request):
    user = request.user

    # Get all messages where the current user is either the sender or receiver
    all_messages_sent = Message.objects.filter(user=user).order_by('-date')
    all_messages_received = Message.objects.filter(receiver=user).order_by('-date')

    # Combine sent and received messages into a single queryset
    all_messages = all_messages_sent | all_messages_received

    # store the latest message for each user
    latest_messages = {}

    # Iterate through messages and keep track of the latest message and unread count for each user
    for message in all_messages:
        if message.user == user:
            other_user = message.receiver
        else:
            other_user = message.user

        # Check if Other User Exists in latest_messages or if the Message is More Recent
        if other_user not in latest_messages or message.date > latest_messages[other_user].date:
            # Update latest_messages with the Current Message
            latest_messages[other_user] = message



    # Get notification counts for the current user as the receiver
    notification_counts_receiver = Notificaton.objects.filter(message__receiver=user,is_seen=False).values('message__user').annotate(count=Count('message__user'))

    unique_users = list(latest_messages.values())
    context = {
        'users': unique_users,
        'notification_counts_receiver': notification_counts_receiver,
    }
    return render(request, 'chat.html', context)



















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

