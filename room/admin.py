from django.contrib import admin

# Register your models here.
from .models import RoomUser,Message
admin.site.register(RoomUser)
admin.site.register(Message)
