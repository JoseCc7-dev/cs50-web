from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class Room(models.Model):
    roomname = models.CharField(max_length=20, unique=True, null=False, blank=False)
    connections = models.IntegerField()

class Chatter(models.Model):
    room  = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Message(models.Model):
    text = models.CharField(max_length=120)
    room = models.ForeignKey(Room, on_delete=models.CASCADE) 
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    time = models.DateTimeField(auto_now_add=True)

# Followers(): temp?
    # foreign key follower
    # foreign key followed