from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from Authuser.models import UserProfile
from django.contrib.auth.models import User 
from .models import Stream,Post,Tag,Like,Comments,Follow,Post_save
from .forms import NewPost

# story modedl
from story.models import Story,StoryStream
# from story.models import get_stories_of_followed_users,get_followed_users
from datetime import datetime


from random import sample


@login_required
def index(request):
    user = request.user
    
    # Get the users that the current user is following
    following_users = Follow.objects.filter(follower=user).values_list('following', flat=True)

    # Filter StoryStream objects based on the followed users
    stories = StoryStream.objects.filter(user__in=following_users)

    # get post for followed user
    posts = Stream.objects.filter(user=user)

    post_stream_ids = []

    for post in posts:
        post_stream_ids.append(post.post.id)

    post_items = Post.objects.filter(id__in=post_stream_ids).order_by('-id')   
    # Fetch comments for each post
    comments = Comments.objects.filter(post__in=post_items)

    saved_post_ids = Post_save.objects.filter(user=user).values_list('post__id', flat=True)
    context = {
        'post_items': post_items,
        'comments': comments,
        'stories': stories,
        'saved_post_ids':saved_post_ids
    }

    return render(request, 'index.html', context)


def create_post(request):

    tag_obj = []
    if request.method == 'POST':
        post_form = NewPost(request.POST, request.FILES)

        if post_form.is_valid():
            picture = post_form.cleaned_data.get('picture')
            caption = post_form.cleaned_data.get('caption')
            tags = post_form.cleaned_data.get('tags')
            tag_list = tags.split(',')

            for tag in tag_list:
                t,create = Tag.objects.get_or_create(title=tag)
                tag_obj.append(t)

            user = request.user
            print(user)     
            p,create = Post.objects.get_or_create(picture=picture, caption=caption, user=user) 
            p.tags.set(tag_obj)   
            p.save()
            return redirect('index') 
    else:
        post_form = NewPost()
        context = {
            'post_form': post_form 
        }
        return render(request, 'post.html', context)
    
    
from django.core.paginator import Paginator

def post_details(request, id):
    post = get_object_or_404(Post, id=id)
    related_posts = Post.objects.filter(tags__in=post.tags.all()).exclude(id=post.id)
    print(related_posts)
    
    paginator = Paginator(related_posts, 10)  # Adjust the number of posts per page as needed
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    comments = Comments.objects.filter(post=post)
    saved_post_ids = Post_save.objects.filter(user=request.user)

    context = {
        'post': post,
        'comments': comments,
        'saved_post_ids': saved_post_ids,
        'page_obj': page_obj,
    }
    return render(request, 'post-details.html', context)  


def like(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        user = request.user

        if user.is_authenticated:
            # Check if the user already liked the post
            liked = Like.objects.filter(user=user, post=post).exists()

            if liked:
                # If liked, remove the like
                post.likes -= 1
                Like.objects.filter(user=user, post=post).delete()
            else:
                # If not liked, add the like
                post.likes += 1
                Like.objects.create(user=user, post=post)

            post.save()

            return JsonResponse({'liked': not liked, 'count': post.likes}, status=200)

    return JsonResponse({}, status=400)


def comment(request, id):
    user = request.user
    # Get the UserProfile of the authenticated user
    user_profile = get_object_or_404(UserProfile, user=user)
    # Get the Post for the given id or return a 404 response if not found
    post = get_object_or_404(Post, id=id)

    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        
        # Check if the comment_text is not empty
        if comment_text:
            # Create a new comment using the UserProfile's user field
            comment = Comments.objects.create(user=user_profile.user, post=post, comment=comment_text)

            context = {
                'user': {
                    'id': user_profile.id,
                    'username': user_profile.user.username,
                    'profile_picture': user_profile.profile_picture.url, 
                },
                'post': post.id,
                'title': post.caption,
                'comment': comment_text,
            }

            return JsonResponse({'data': context})
        else:
            return JsonResponse({'error': 'Comment cannot be empty'})

    return JsonResponse({'error': 'Invalid request'})


def save_post(request, id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=id)
        user = request.user

        if user.is_authenticated:
            # Check if the user already saved the post
            saved = Post_save.objects.filter(user=user, post=post).exists()

            if saved:
                # If already saved, delete the saved instance
                Post_save.objects.filter(user=user, post=post).delete()
                return JsonResponse({'message': 'Post removed from saved.'})
            else:
                # If not saved, create a new saved instance
                Post_save.objects.create(user=user, post=post)
                return JsonResponse({'message': 'Post saved successfully.'})
        else:
            return JsonResponse({'error': 'Authentication required.'}, status=401)

    return JsonResponse({'error': 'Method not allowed.'}, status=405)


def profile(request):
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)

    # Count the number of users the current user is following
    following_count = Follow.objects.filter(follower=user).count()

    # Count the number of users following the current user
    followers_count = Follow.objects.filter(following=user).count()

    post = Post.objects.filter(user=user)

    context = {
        'user_profile': user_profile,
        'user':user,
        'posts': post,
        'following_count': following_count,
        'followers_count': followers_count,
    }
    return render(request, 'profile.html', context)


def followers(request, id):
    user = User.objects.get(id=id)
    following = Follow.objects.filter(following=user)

    followers_with_status = []
    for follow in following:
        follower = follow.follower
        follow_status = Follow.objects.filter(following=follower, follower=request.user).exists()
        followers_with_status.append({'follower': follower, 'follow_status': follow_status})

    print(followers_with_status)  # Check if this prints data in your console

    context = {
        'followers_with_status': followers_with_status,
    }
    return render(request, 'followers.html', context)


def following(request, id):
    user = get_object_or_404(User, id=id)
    followers = Follow.objects.filter(follower=user)

    following_with_status = []
    for follow in followers:
        following_user = follow.following
        follow_status = Follow.objects.filter(following=following_user, follower=request.user).exists()
        following_with_status.append({'following': following_user, 'follow_status': follow_status})

    print(following_with_status)  # Check if this prints data in your console

    context = {
        'following_with_status': following_with_status,
    }
    return render(request, 'follow.html', context)


def get_other_user(request, id):
    user = get_object_or_404(User, id=id)

    user_profile = UserProfile.objects.get(user=user)
    print(user_profile)
    
    follow_status = Follow.objects.filter(following=user, follower=request.user).exists()

    following_count = Follow.objects.filter(follower=user).count()

    # Count the number of users following the current user
    followers_count = Follow.objects.filter(following=user).count()

    posts = Post.objects.filter(user=user)

    context = {
        'user_profile': user_profile,
        'user' : user,
        'posts': posts,
        'follow_status': follow_status,
        'following_count': following_count,
        'followers_count': followers_count,
    }

    return render(request, 'user_profile.html', context )


def follow_unfollow(request, user_id):
    target_user = get_object_or_404(User, id=user_id)

    try:
        # Check if the user is already following the target user
        follow = Follow.objects.get(follower=request.user, following=target_user)
        print(follow)
        # If yes, unfollow
        follow.delete()
        is_following = False

        # Remove posts from the unfollowed user from the user's stream
        Stream.objects.filter(user=request.user, following=target_user).delete()
    except Follow.DoesNotExist:
        # If not, follow
        follow = Follow(follower=request.user, following=target_user)
        follow.save()

        # Add posts from the followed user to the user's stream
        posts_from_target_user = Post.objects.filter(user=target_user)
        for post in posts_from_target_user:
            new_stream_item = Stream(user=request.user, post=post, date=post.posted, following=target_user)
            new_stream_item.save()

        is_following = True
        
    # Get follower and following counts
    followers_count = Follow.objects.filter(following=target_user).count()
    following_count = Follow.objects.filter(follower=target_user).count()

    # You can return a JsonResponse to update the UI dynamically
    return JsonResponse({'is_following': is_following, 'followers_count': followers_count, 'following_count': following_count})


def explore(request):
    # Get all posts
    all_posts = Post.objects.all()
    
    # Get random posts
    random_posts = sample(list(all_posts), Post.objects.count())

    # Check if there's a search query in the GET parameters
    search_results = []
    search_query = request.GET.get('search_query')
    if search_query:
        # Filter user profiles based on the search query
        search_results = UserProfile.objects.filter(user__username__icontains=search_query)
        random_posts = None

    else:
        search_results = []

    context = {
        'random_posts': random_posts,
        'user_profiles': search_results,
    }
    return render(request, 'explore.html', context)


def search_users(request):
    query = request.GET.get('query')
    if query:
        search_results = UserProfile.objects.filter(user__username__icontains=query)[:10]  # Limit results to 10
        return render(request, 'search_result.html', {'search_results': search_results})
    else:
        return render(request, 'search_result.html', {'search_results': []})






# def index(request):
#     user = request.user
    
#     stories = StoryStream.objects.filter(user=user)
#     print(stories)

#     # get post for followed user
#     posts = Stream.objects.filter(user=user)

#     post_stream_ids = []

#     for post in posts:
#         post_stream_ids.append(post.post.id)

#     post_items = Post.objects.filter(id__in=post_stream_ids).order_by('-id')   
#     # print(post_items,'post_item') 

#     # Fetch comments for each post
#     comments = Comments.objects.filter(post__in=post_items)
    
#     context = {
#         'post_items': post_items,
#         'comments': comments,
#         'stories':stories
#     }

#     return render(request, 'index.html', context)
    


