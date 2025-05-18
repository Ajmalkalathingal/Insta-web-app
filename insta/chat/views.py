from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Message,Notificaton,ChatGroup
from django.contrib.auth.models import User
from django.db.models import Count 
from django.db.models import Q
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db.models import Max, Q, Count



@login_required
def main_chat(request, group_name=None, user_id=None):
    users = User.objects.exclude(id=request.user.id)
    messages = []
    thread_name = None
    receiver = None

    if group_name:
        thread_name = group_name
        messages = Message.objects.filter(theard_name=thread_name)
    
    elif user_id:
        user_obj = get_object_or_404(User, id=user_id)
        receiver = user_obj

        # Build private thread name like 'private_3-5'
        if request.user.id > user_obj.id:
            room_name = f'{request.user.id}-{user_obj.id}'
        else:
            room_name = f'{user_obj.id}-{request.user.id}'
        
        thread_name = f'private_{room_name}'
        print(thread_name,"thread name message")
        messages = Message.objects.filter(theard_name=thread_name)
    
    else:
        return redirect('home')

    # Mark messages as read
    messages.update(is_read=True)
    print(messages)
    # Mark related notifications as seen
    Notificaton.objects.filter(
        message__in=messages,
        receiver=request.user,
        is_seen=False
    ).update(is_seen=True)

    context = {
        'users': users,
        'messages': messages,
        'today': timezone.now().date(),
        'receiver': receiver,
        'thread_name': thread_name,
        'group_name': group_name,
    }

    return render(request, 'message.html', context)


def chatt(request):
    user = request.user

    # Get latest message per conversation pair
    messages = Message.objects.filter(
        Q(user=user) | Q(receiver=user)
    ).order_by('-date')

    latest_messages = {}
    for message in messages:
        other_user = message.receiver if message.user == user else message.user
        if other_user not in latest_messages:
            latest_messages[other_user] = message  # first one is latest due to ordering

    notification_counts_receiver = (
        Notificaton.objects.filter(
            receiver=user,
            is_seen=False
        )
        .values('user')  # sender
        .annotate(count=Count('id'))
    )
    context = {
        'users': list(latest_messages.values()),
        'notification_counts_receiver': notification_counts_receiver,
    }

    return render(request, 'new_chat.html', context)



def load_users(request):
    users = User.objects.all()
    print(users,'userfrhgyguijghogy')
    return render(request, 'userList.html', {'users': users})





def chat(request):
    user = request.user

    # Get all private messages (1-to-1 conversations)
    private_messages = Message.objects.filter(
        Q(user=user) | Q(receiver=user),
        group__isnull=True  # Only private messages (no group)
    ).order_by('-date')

    latest_private = {}
    for msg in private_messages:
        other_user = msg.receiver if msg.user == user else msg.user
        if other_user.id not in latest_private:
            latest_private[other_user.id] = {
                'type': 'private',
                'other_user': other_user,
                'message': msg
            }

    # Get latest message per group the user is in
    group_messages = Message.objects.filter(
        group__members=user).values('group') .annotate(latest_date=Max('date')).order_by('-latest_date')
    group = ChatGroup.objects.all()

    latest_group = []
    for gm in group_messages:
        latest_msg = Message.objects.filter(group_id=gm['group'], date=gm['latest_date']).first()
        latest_group.append({
            'type': 'group',
            'group': latest_msg.group,
            'message': latest_msg
        })

    # Get notification counts for the receiver
    notification_counts_receiver = Notificaton.objects.filter(
        receiver=user,
        is_seen=False
    ).values('user').annotate(count=Count('id'))

    context = {
        'private_chats': list(latest_private.values()),
        'group_chats': latest_group,
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

