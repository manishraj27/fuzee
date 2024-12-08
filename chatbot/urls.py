from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home_view, name='home'),  # This should be the first route
    path('chat/', views.chat_view, name='chat'),
]
