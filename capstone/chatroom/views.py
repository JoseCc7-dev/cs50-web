import json
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Room, Message

# Create your views here.
def index(request):
    rooms = Room.objects.filter()
    return render(request, "chatroom/index.html", {
        "rooms":rooms
    })

def register(request):
    if request.method == "POST":
        username = request.POST["username"].strip()

        if request.POST["password"] == request.POST["confirm_password"]:
            password = request.POST["password"]

        try:
            user = User.objects.create_user(username, None, password)
        except IntegrityError:
            return render(request, "chatroom/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "chatroom/register.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"].strip()
        password = request.POST["password"]
        user = authenticate(request, username = username, password = password)
        
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "chatroom/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "chatroom/login.html")

def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def load_chatroom(request, room_name):
    if request.user.is_authenticated:
        room = Room.objects.get(roomname = room_name)
        messages = Message.objects.filter(room_id = room.id).order_by('time')
        messages_and_bool = []
        for i in range(len(messages)):
            curruser = False
            if messages[i].user_id == request.user.id:
                curruser = True
            templist = []
            templist.append(messages[i])
            templist.append(curruser)
            messages_and_bool.append(templist)
        return render(request, "chatroom/chatroom.html", {
            "messages_and_bool": messages_and_bool, "room_name": room
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def new_message(request):
    body = json.loads(request.body.decode('utf-8'))
    room_id = Room.objects.get(roomname = body['room'][1:-1]).id
    user_id = User.objects.get(username = body['user']).id
    msg = Message.objects.create(text = body['text'], room_id = room_id, user_id = user_id, time = datetime.now())
    return HttpResponse(status=204)
