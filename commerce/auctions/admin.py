from django.contrib import admin

from .models import User, listings, watchlist, comments
# Register your models here.

admin.site.register(User)
admin.site.register(listings)
admin.site.register(watchlist)
admin.site.register(comments)