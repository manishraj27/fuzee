# routing.py
from django.urls import path
from room import consumers

websocket_urlpatterns = [
    path('ws/messages/<str:room_id>/<str:username>/', consumers.ChatConsumer.as_asgi()), #you have to do wss while deployment since it will be https
]
