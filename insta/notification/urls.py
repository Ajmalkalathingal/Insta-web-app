from django.urls import path 
from . import views

urlpatterns = [
    path('',views.notification_view,name='notification'),
    path('delete/<int:id>',views.del_notification,name='delete'),
   



]