from django.urls import path
from . import views



urlpatterns = [
    path('', views.CreateRoomView, name='home'),  # Use CreateRoomView for home if it handles room creation
    path('room/', views.CreateRoomView, name='room'),
    path('join-room/', views.JoinRoomView, name='join_room'),
    path('room/<str:room_id>/<str:username>/', views.RoomView, name='room'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
]  
