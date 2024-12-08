from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .import views



urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('register/',views.register,name='register'),
    path('loginn/',views.loginn,name='loginn'),
    path('logout/',views.logout,name='logout'),
    path('index/',views.index,name='index'),
    path('upload/',views.upload,name='upload'),
    path('setting/',views.setting,name='setting'),
    path('like-post/', views.like_post, name='like_post'),
    path('profile/<str:pk>/', views.profile, name='profile'),
    path('follow', views.follow, name='follow'),
    path('search', views.search, name='search'),
    path('delete_post/<uuid:post_id>/', views.delete_post, name='delete_post'),
    path('add-comment/<uuid:pk>/', views.add_comment, name='add-comment'),
    path('delete-comment/<uuid:comment_id>/', views.delete_comment, name='delete_comment'),
]   

