from django.urls import path 
from . import views

urlpatterns = [
    path('<int:user_id>/',views.main_chat,name='main_chat'),
    path('chat/',views.chat, name='chat'),
    # path('mark_notifications_as_seen/<int:user_id>/', views.mark_notifications_as_seen, name='mark_notifications_as_seen'),



]