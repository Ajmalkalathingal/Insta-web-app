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



# def view_story(request, username, story_id):
    
#     user = get_object_or_404(User, username=username)
    
#     # Get the current user's stories
#     user_stories = Story.objects.filter(user=user).order_by('posted')
    
#     # Get the users that the current user is following
#     following_users = Follow.objects.filter(follower=request.user).values_list('following', flat=True)
    
#     # Filter StoryStream objects based on the followed users
#     users_with_stories = StoryStream.objects.filter(user__in=following_users)
    
#     previous_story = None
#     next_story = None
#     next_user = None
    
#     # Find the index of the current story
#     current_story_index = None
#     for i, story in enumerate(user_stories):
#         if story.id == story_id:
#             current_story_index = i

#         # Get the current user's story
#         if current_story_index is not None:
#             user_story = user_stories[current_story_index]
        
#             # Calculate previous and next stories for the current user's stories
#             previous_story = user_stories[current_story_index - 1] if current_story_index > 0 else None
#             next_story = user_stories[current_story_index + 1] if current_story_index < len(user_stories) - 1 else None


#     context = {
#         'user': user,
#         'users_with_stories': users_with_stories,
#         'user_story': user_stories[current_story_index] if current_story_index is not None else None,
#         'previous_story': previous_story,
#         'next_story': next_story
#     }
    
#     return render(request, 'view_story.html', context)


from django.db.models import Max

def view_story(request, username, story_id):
    user = get_object_or_404(User, username=username)
    
    # Get the current user's stories
    user_stories = Story.objects.filter(user=user).order_by('posted')

    # Get the users that the current user is following
    following_users = Follow.objects.filter(follower=request.user).values_list('following', flat=True)

    # Filter StoryStream objects based on the followed users
    story_streams = StoryStream.objects.filter(user__in=following_users).order_by('date')

    # Find the index of the current story
    current_story_index = None
    user_story = None
    previous_story = None
    next_story = None
    next_user_story_stream = None

    for story_stream in story_streams:
        for i, story in enumerate(story_stream.story.all()):
            if story.id == int(story_id):
                current_story_index = i
                break  # Exit loop once the story is found

        if current_story_index is not None:
            break  # Exit outer loop if current_story_index is found

    # Get the current user's story
    if current_story_index is not None:
        user_story = user_stories[current_story_index]
        
        # Calculate previous and next stories for the current user's stories
        previous_story = user_stories[current_story_index - 1] if current_story_index > 0 else None
        next_story = user_stories[current_story_index + 1] if current_story_index < len(user_stories) - 1 else None
    else:
        # Find the next user's story
        next_user_story_stream = story_streams.filter(date__gt=user_stories.aggregate(Max('posted'))['posted__max']).first()
        if next_user_story_stream:
            next_user_story = next_user_story_stream.story.first()
            if next_user_story:
                # Set next_user_story_stream as next user's story stream
                user_story = user_stories[0] if user_stories else None  # First story of the next user

    # Get the previous user's story
    if previous_story is None and current_story_index is None:
        previous_story_index = len(user_stories) - 1
        previous_story = user_stories[previous_story_index] if previous_story_index >= 0 else None

    context = {
        'story_streams': story_streams,
        'user': user,
        'user_story': user_story,
        'previous_story': previous_story,
        'next_story': next_story,
        'next_user': next_user_story_stream.user if next_user_story_stream else None
    }

    return render(request, 'view_story.html', context)



# def view_story(request, username, story_id):
#     user = get_object_or_404(User, username=username)
#     stories = Story.objects.filter(user=user).order_by('posted')
#     context = {'user': user, 'stories': stories}
#     return render(request, 'view_story.html', context)


# def next_story(request):
#     # Implement logic to fetch the data for the next story
#     # For example, you could retrieve the next story from the database
#     next_story = Story.objects.filter(...).first()  # Adjust the filtering logic as needed
#     print(next_story,'next')
#     # Prepare the data to be returned in JSON format
#     if next_story:
#         data = {
#             'content_url': next_story.content.url,
#             # Add other fields as needed
#         }
#         return JsonResponse(data)
#     else:
#         return JsonResponse({'error': 'No next story found'}, status=404)

