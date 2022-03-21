from email.policy import default
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

# TODO
# Listing creator
# Bid winner
# Comments
class listings(models.Model):
    title = models.CharField(max_length=40, unique=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing_creator")
    category = models.CharField(max_length=30)
    description = models.CharField(max_length=400)
    imageurl = models.CharField(max_length=90)
    starting_bid = models.IntegerField(default=1)
    current_bid = models.IntegerField(default=0, blank=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="bid_winner")
    active = models.BooleanField(default=True) 

class watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(listings, on_delete=models.CASCADE, unique=True)

# class bids(models.Model):
#     amount = models.IntegerField()

class comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(listings, on_delete=models.CASCADE)
    text = models.CharField(max_length= 120)

