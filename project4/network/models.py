from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=280)
    timestamp = models.DateTimeField()

class like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(post, on_delete=models.CASCADE)

class follower(models.Model):
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed_user")
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower_user")