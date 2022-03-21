from django.urls import path

from . import views

urlpatterns = [
    path("", views.default, name="redirect"),
    path("<int:pg_num>", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    # API Routes
    path("like/<int:post_id>", views.like_post, name="like_post"),
    path("edit/<int:post_id>", views.edit_post, name="edit_post"),
    
    path("following/<int:pg_num>", views.load_following, name="following"),
    path("<str:name>/<int:pg_num>", views.load_profile, name="profile"),

    
    
    
]
