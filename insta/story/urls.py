
from django.urls import path
from . import views


app_name = "story"

urlpatterns = [
    path('upload/', views.upload_story, name='upload_story'),
    path('viewer/<int:user_id>/', views.view_user_stories, name='view_user_stories'),
    path('fetch/<int:user_id>/', views.fetch_user_stories, name='fetch_user_stories'),

]


