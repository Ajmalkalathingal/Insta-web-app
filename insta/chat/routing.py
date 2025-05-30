from django.urls import path
from chat import consumers

websocket_urlpatterns = [
     path('ws/<int:id>/', consumers.MyAsyncWebsocketConsumer.as_asgi()),
     path('ws/notification/', consumers.NotificationConsumer.as_asgi()),
]
