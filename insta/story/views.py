from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Story,StoryStream
from main.models import Follow

from django.db.models import Count


def create_story(request):
    if request.method == 'POST':
        # Handle form submission
        user = request.user
        content = request.FILES.get('content')
        expiration_time = timezone.now() + timezone.timedelta(hours=24)  # Example: set expiration time to 24 hours from now
        Story.objects.create(user=user, content=content, expiration_time=expiration_time)
        return redirect('index')  # Redirect to home page after story creation
    else:
        return render(request, 'create_story.html')




# def view_story(request, username, story_id=None):
#     user = get_object_or_404(User, username=username)
#     user_stories = Story.objects.filter(user=user).order_by('posted')

#     previous_story = None
#     next_story = None
    
#     # Find the index of the current story
#     current_story_index = None
#     for i, story in enumerate(user_stories):
#         if story.id == story_id:
#             current_story_index = i
#             break
    
#     # Calculate previous and next stories
#     if current_story_index is not None:
#         if current_story_index > 0:
#             previous_story = user_stories[current_story_index - 1]
#         if current_story_index < len(user_stories) - 1:
#             next_story = user_stories[current_story_index + 1]

#     # Check if there is a next story available
#     if next_story is None:
#         # Find the username of the next story's owner
#         next_username = user_stories[current_story_index + 1].user.username
#         # Redirect to the same story under the context of the next user
#         return redirect('view_story', username=next_username, story_id=story_id)

#     context = {
#         'user': user,
#         'user_stories': user_stories,
#         'user_story': user_stories[current_story_index],  # Directly fetch the current story
#         'previous_story': previous_story,
#         'next_story': next_story
#     }
#     return render(request, 'view_story.html', context)


def view_story(request, username, story_id):
    
    user = get_object_or_404(User, username=username)
    
    # Get the current user's stories
    user_stories = Story.objects.filter(user=user).order_by('posted')
    
    # Get the users that the current user is following
    following_users = Follow.objects.filter(follower=request.user).values_list('following', flat=True)
    
    # Filter StoryStream objects based on the followed users
    users_with_stories = StoryStream.objects.filter(user__in=following_users).annotate(num_stories=Count('story')).filter(num_stories__gt=0)
    
    previous_story = None
    next_story = None
    next_user = None
    
    # Find the index of the current story
    current_story_index = None
    for i, story in enumerate(user_stories):
        if story.id == story_id:
            current_story_index = i
            break

    # Get the current user's story
    if current_story_index is not None:
        user_story = user_stories[current_story_index]
    
        # Calculate previous and next stories for the current user's stories
        previous_story = user_stories[current_story_index - 1] if current_story_index > 0 else None
        next_story = user_stories[current_story_index + 1] if current_story_index < len(user_stories) - 1 else None

        
    # Check if next_story is None and handle accordingly
    if next_story is None and current_story_index < len(user_stories) - 1:
        # Get the next user's story
        next_user_story = StoryStream.objects.filter(date__gt=user_story.posted, user=user).order_by('date').first()
        print(next_user_story)
        
        if next_user_story:
            next_user = next_user_story.following
            next_user_stories = next_user_story.story.all().order_by('posted')
            next_story = next_user_stories.first() if next_user_stories else None
            next_story_id = next_story.id if next_story else None
            print("Redirecting to next user's story:", next_user, next_story_id)
            return redirect('view_story', username=next_user.username, story_id=next_story_id)
        else:
            print("No next user story found.")
            # Handle the case when there are no more stories for the current user and no more users with stories
            # You can redirect to a different page or display a message indicating that there are no more stories available
            return render(request, 'index.html')

    context = {
        'user': user,
        'users_with_stories': users_with_stories,
        'user_story': user_stories[current_story_index] if current_story_index is not None else None,
        'previous_story': previous_story,
        'next_story': next_story
    }
    
    return render(request, 'view_story.html', context)





#   print("Current story index:", current_story_index)
#     print("Total number of user stories:", len(user_stories))
#     print("Is current story index less than the total number of stories minus 1?", current_story_index < len(user_stories) - 1)

    # print('next user', next_user)
    # print('previous_story', previous_story)
    # print('next_story', next_story)