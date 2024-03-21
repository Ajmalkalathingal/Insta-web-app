
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('create-post/',views.create_post,name='create-post'),
    path('detail/<int:id>',views.post_details, name='details'),

    # post like
    path('toggle-like/<int:post_id>/', views.like, name='toggle_like'),
    # post comment
    path('comment/<int:id>',views.comment, name='comment'),
    # post save
    # path('savepost/<int:post_id>',views.save_post, name='savepost'),

    # get followers
    path('followers/<int:id>',views.followers, name='followers'),
    # get follow user
    path('follow/<int:id>',views.following, name='follow'),

    path('profile',views.profile, name='profile'),
    path('user/<int:id>',views.get_other_user, name='user'),
    path('follow_unfollow/<int:user_id>/', views.follow_unfollow, name='follow_unfollow'),

    path('explore/',views.explore,name='explore'),
    path('search/',views.search_users,name='search'),

    path('save-post/<int:id>/',views.save_post, name='save-post'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)































# def comment(request, id):
#     user = request.user
#     post = Post.objects.get(id=id)

#     if request.method == 'POST':
#         comment_text = request.POST.get('comment')
#         save_comment = Comments.objects.create(user=user, post=post, comment=comment_text)

#         context = {
#             'user': {
#                 'id': user.id,
#                 'username': user.username,
#                 # 'profile_picture': str(user.userprofile.profile_picture.url), 
#             },
#             'post': post.id,
#             'title': post.caption,
#             'comment': comment_text,
#         }

#         return JsonResponse({'data': context})

#     return JsonResponse({'error': 'Invalid request'})


# <!-- {% extends 'base.html' %}
# {% load static %}
# {% block content %}
# <h1>followers</h1>
# {% for follow in followers %}
# <div class="cotainer">
#     <div class="row">
#         <div class="col-md-3"></div>
#         <div class="col-md-6 mt-4">
#             <div class="d-flex align-items-start pb-2">
#                 <a href="{% url 'user' follow.follower.id %}">cli</a><img src="{{follow.follower.userprofile.profile_picture.url}}" class="rounded-circle mr-3" alt="img" width="60" height="60">
#                 <div class="flex-grow-1">
#                     <h6 class="mb-0"><b></b></h6>
#                     <div class="small text-muted container pt-4"><span class="fas fa-circle chat-online"></span> {{follow.follower}}</div>
                    
#                     {% if follow_status == True %}
#                     <button class="follow-unfollow-btn  profile-edit-btn" style="color: rgb(0, 128, 255);" data-user-id="{{ follow.follower.id }}" onclick="followUnfollow(this)">Unfollow</button>
#                 {% else %}
#                     <button class="follow-unfollow-btn  profile-edit-btn" style="color: rgb(0, 128, 255);" data-user-id="{{ follow.follower.id }}" onclick="followUnfollow(this)">Follow</button>
#                 {% endif %}
                
#             </div>
#         </div>
#         <div class="col-md-3"></div>
#     </div>
# </div>
# {% endfor %}
# {% endblock content %} -->