from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Story
from main.models import Follow
from .forms import StoryForm
from django.contrib.auth.decorators import login_required
from django.utils.timesince import timesince
from django.utils.timezone import now
from django.http import JsonResponse


@login_required
def upload_story(request):
    if request.method == 'POST':
        form = StoryForm(request.POST, request.FILES)
        if form.is_valid():
            story = form.save(commit=False)
            story.user = request.user
            story.save()
            return redirect('index')
    else:
        form = StoryForm()
    return render(request, 'stories/upload.html', {'form': form})


@login_required
def view_user_stories(request, user_id):
    all_users = Follow.objects.filter(follower=request.user).values_list('following', flat=True)
    all_users_with_story = list(User.objects.filter(id__in=all_users, stories__expires_at__gt=timezone.now()).distinct())

    user_ids = [u.id for u in all_users_with_story]

    context = {
        'user_ids': user_ids,
        'start_user_id': user_id
    }
    return render(request, 'stories/story_viewer.html', context)

@login_required
def fetch_user_stories(request, user_id):
    user = get_object_or_404(User, id=user_id)
    stories = Story.objects.filter(user=user, expires_at__gt=timezone.now()).order_by('-created_at')

    story_data = [{
        'media_url': story.media.url,
        'caption': story.caption,
        'created': timesince(story.created_at, now()) + ' ago'
    } for story in stories]
    print(story_data, 'story data')
    return JsonResponse({
        'username': user.username,
        'profile_picture': user.userprofile.get_profile_picture_url,
        'stories': story_data
    })




