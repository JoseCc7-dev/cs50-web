from unicodedata import name
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("newpage", views.newPage, name="newPage"),
    path("randompage", views.randomPage, name="randomPage"),
    path("search", views.search, name="search"),
    path("edit/", views.editPage, name="editPage"),
    path("<str:entry>", views.loadPage, name="loadPage"),
]
