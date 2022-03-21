from django.contrib import admin
from .models import User, follower, post, like

# Register your models here.

admin.site.register(User)
admin.site.register(post)
admin.site.register(like)
admin.site.register(follower)