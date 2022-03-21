from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_user, name="logout"),
    # API Routes
    path("send", views.new_message, name="message"),
    
    path("<str:room_name>/", views.load_chatroom, name="chatroom"),
    # path("user/<str:name>", views.load_user, name="user"),
    
    
    
]