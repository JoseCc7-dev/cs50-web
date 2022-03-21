from os import name
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newlisting", views.new_listing, name="newlisting"),
    path("watchlist", views.loadwatchlist, name="watchlist"),
    path("categories", views.loadcategories, name="categories"),
    path("<str:listing>", views.load, name="load"),
    
]
