from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    room_id = models.CharField(max_length=6, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.room_id

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender = models.CharField(max_length=225)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.room} - {self.sender}"

class RoomUser(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    username = models.CharField(max_length=255)
    connected_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('room', 'username')  # Ensure a user can't be added to the same room multiple times

    def __str__(self):
        return f"{self.username} in {self.room}"
    
