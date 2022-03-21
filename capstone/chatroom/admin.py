from email import message
from django.contrib import admin

from .models import User, Room, Chatter, Message

# Register your models here.

admin.site.register(User)
admin.site.register(Room)
admin.site.register(Chatter)
admin.site.register(Message)