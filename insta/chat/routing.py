from django.urls import path
from chat import consumers

websocket_urlpatterns = [
     path('ws/<int:id>/', consumers.MyAsyncWebsocketConsumer.as_asgi(), {'chat_type': 'private'}),
      path('ws/<str:group_name>/', consumers.MyAsyncWebsocketConsumer.as_asgi(), {'chat_type': 'group'}),
     path('ws/notification/', consumers.NotificationConsumer.as_asgi()),
]
