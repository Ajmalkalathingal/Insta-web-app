import pytest
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from story.models import Story, Follow

@pytest.mark.django_db
def test_story_viewer_only_shows_following_users_with_valid_stories(client, django_user_model):
    # Create two users
    user1 = django_user_model.objects.create_user(username='user1', password='pass')
    user2 = django_user_model.objects.create_user(username='user2', password='pass')
    
    # Log in as user1
    client.login(username='user1', password='pass')

    # Make user1 follow user2
    Follow.objects.create(follower=user1, following=user2)

    # Create a valid story for user2
    Story.objects.create(
        user=user2,
        media='media/sample.jpg',
        caption='A test story',
        expires_at=timezone.now() + timedelta(hours=1)
    )

    url = reverse('story:view_user_stories', args=[user2.id])
    response = client.get(url)
    
    assert response.status_code == 200
    assert str(user2.id) in response.content.decode()

@pytest.mark.django_db
def test_fetch_user_stories_excludes_expired(client, django_user_model):
    user = django_user_model.objects.create_user(username='storyuser', password='pass')
    client.login(username='storyuser', password='pass')

    # Create story: 1 valid, 1 expired
    Story.objects.create(
        user=user,
        media='media/valid.jpg',
        caption='Valid story',
        expires_at=timezone.now() + timedelta(hours=1)
    )
    Story.objects.create(
        user=user,
        media='media/expired.jpg',
        caption='Expired story',
        expires_at=timezone.now() - timedelta(hours=1)
    )

    url = reverse('story:fetch_user_stories', args=[user.id])
    response = client.get(url)
    data = response.json()

    assert response.status_code == 200
    assert len(data['stories']) == 1
    assert data['stories'][0]['caption'] == 'Valid story'
