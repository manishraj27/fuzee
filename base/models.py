from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
import uuid
from datetime import datetime
from froala_editor.fields import FroalaField

User = get_user_model()

##CREATE PROFILE MODEL##############
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to Django's User model
    id_user=models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_pic',default='blank-profile-picture.png')
    location = models.CharField(max_length=100, blank=True)
    

    def __str__(self):
        return self.user.username
    
###########CREATE AND UPLOAD POST###########
    
class Post(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4)
    user=models.CharField(max_length=100)
    content = FroalaField(null=True, blank=True)
    image = models.ImageField(upload_to='post_images')
    caption =models.TextField(null=True, blank=True)
    create_at =models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.user
    

################LIKE POST################

class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)
    
    def __str__(self):
        return self.username
    
    
#######FOLLOWERS###########

class FollowersCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user

import uuid
from django.db import models
from datetime import datetime

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Use UUIDField for id
    user = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(blank=True, default=datetime.now)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return self.content[:20]  # Display first 20 characters of content

