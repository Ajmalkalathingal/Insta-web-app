import pytest
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from chat.models import Message, Notificaton
from Authuser.models import UserProfile
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.mark.django_db
def test_main_chat_view(client):
    # Create users
    sender = User.objects.create_user(username='sender', password='pass')
    receiver = User.objects.create_user(username='receiver', password='pass')

    # Create user profiles
    UserProfile.objects.get_or_create(user=sender)
    UserProfile.objects.get_or_create(user=receiver)

    # Login sender
    client.login(username='sender', password='pass')

    # Determine thread name
    thread = f'chat_{max(sender.id, receiver.id)}-{min(sender.id, receiver.id)}'

    # Create a message from sender to receiver
    msg = Message.objects.create(
        user=sender,
        receiver=receiver,
        message="Hello",
        theard_name=thread,
        is_read=False,
        date=timezone.now()
    )

    # Notification for the logged-in user (sender is receiver in this case)
    notif = Notificaton.objects.create(
        user=receiver,          
        receiver=sender,        # the logged-in user
        message=msg,
        is_seen=False
    )

    url = reverse('main_chat', args=[receiver.id])
    response = client.get(url)
    print(response)
    assert response.status_code == 200

    # Message should be marked as read
    msg.refresh_from_db()
    assert msg.is_read is True

    # Notification should be marked as seen
    notif.refresh_from_db()
    assert notif.is_seen is True


@pytest.mark.django_db
def test_chat_view(client):
    user1 = User.objects.create_user(username='user1', password='pass')
    user2 = User.objects.create_user(username='user2', password='pass')

    test_image1 = SimpleUploadedFile("test1.jpg", b"fakeimagecontent", content_type="image/jpeg")
    test_image2 = SimpleUploadedFile("test2.jpg", b"fakeimagecontent", content_type="image/jpeg")

    user1.userprofile.profile_picture = test_image1
    user1.userprofile.save()

    user2.userprofile.profile_picture = test_image2
    user2.userprofile.save()

    client.login(username='user1', password='pass')

    msg = Message.objects.create(
        user=user2,
        receiver=user1,
        message='Hi there!',
        theard_name='chat_test',
        date=timezone.now()
    )

    notif = Notificaton.objects.create(
        user=user2,
        receiver=user1,
        message=msg,
        is_seen=False
    )

    url = reverse('chat')
    response = client.get(url)
    print(response)

    assert response.status_code == 200
    assert 'user2' in response.content.decode()

