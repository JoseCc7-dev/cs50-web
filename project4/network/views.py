from datetime import datetime, timedelta
import sqlite3
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .models import User, follower, like, post
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

def default(request):
    return HttpResponseRedirect("/1")


def index(request, pg_num = 1):
    if request.method == ("POST"):
        conn = sqlite3.connect('db.sqlite3')
        c = conn.cursor()
        poster = User.objects.get(username = request.user)
        if not request.POST["content"]:
            return HttpResponse("Cannot Post Empty Post")
        else:
            content = request.POST["content"]
        timestamp = str(datetime.now() + timedelta(hours = 8))[:19]
        sql = "INSERT INTO network_post(poster_id, text, timestamp) VALUES(?, ?, ?)"
        c.execute(sql, (poster.id, content, timestamp,))
        conn.commit()
        c.close()
        posts = post.objects.order_by('-timestamp')
        posts_and_likes = []
        likes = []
        for i in range(len(posts)):
            likes.append(like.objects.filter(post_id = posts[i].id).count())
            templist = []
            templist.append(posts[i])
            templist.append(likes[i])
            posts_and_likes.append(templist)
        pagination = Paginator(posts_and_likes, 10)
        return render(request, "network/index.html", {
            "posts_and_likes":pagination.page(pg_num), "pg_num":pg_num, "last": last
        })
    else:
        posts = post.objects.order_by('-timestamp')
        posts_and_likes = []
        likes = []
        for i in range(len(posts)):
            likes.append(like.objects.filter(post_id = posts[i].id).count())
            templist = []
            templist.append(posts[i])
            templist.append(likes[i])
            posts_and_likes.append(templist)
        pagination = Paginator(posts_and_likes, 10)
        if pg_num == pagination.num_pages:
            last = True
        else:
            last = False
        return render(request, "network/index.html", {
            "posts_and_likes":pagination.page(pg_num), "pg_num":pg_num, "last": last
        })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def load_profile(request, name, pg_num = 1):
    if request.method == "POST":
        poster = User.objects.get(username= name)
        posts = post.objects.filter(poster_id = poster.id).order_by('-timestamp')
        posts_and_likes = []
        likes = []
        for i in range(len(posts)):
            likes.append(like.objects.filter(post_id = posts[i].id).count())
            templist = []
            templist.append(posts[i])
            templist.append(likes[i])
            posts_and_likes.append(templist)
        pagination = Paginator(posts_and_likes, 10)
        if pg_num == pagination.num_pages:
            last = True
        else:
            last = False        
        if str(request.user) == str(poster.username):
            followable = False
        else:
            followable = True
        conn = sqlite3.connect('db.sqlite3')
        c = conn.cursor()
        if poster.id == request.user.id:
            follower_count = follower.objects.filter(followed = poster.id).count()
            following_count = follower.objects.filter(follower = poster.id).count()
            return render(request, "network/profile.html", {
            "poster":poster, "posts_and_likes":pagination.page(pg_num), "follower_count":follower_count, "follow_count":following_count, "followable":followable, "pg_num":pg_num, "last": last
        })
        if request.POST.get("Follower_action") == "Follow":
            sql = "INSERT INTO network_follower(followed_id, follower_id) VALUES(?, ?)"
            c.execute(sql, (poster.id, request.user.id))
            conn.commit()
            c.close()
            following = True
        elif request.POST.get("Follower_action") == "Unfollow":
            sql = "DELETE FROM network_follower WHERE (followed_id = ? AND follower_id = ?)"
            c.execute(sql, (poster.id, request.user.id))
            conn.commit()
            c.close()
            following = False
        follower_count = follower.objects.filter(followed = poster.id).count()
        following_count = follower.objects.filter(follower = poster.id).count()
        return render(request, "network/profile.html", {
            "poster":poster, "posts_and_likes":pagination.page(pg_num), "follower_count":follower_count, "follow_count":following_count, "followable":followable, "following":following, "pg_num":pg_num, "last": last
        })
    else:
        poster = User.objects.get(username= name)
        posts = post.objects.filter(poster_id = poster.id).order_by('-timestamp')
        posts_and_likes = []
        likes = []
        for i in range(len(posts)):
            likes.append(like.objects.filter(post_id = posts[i].id).count())
            templist = []
            templist.append(posts[i])
            templist.append(likes[i])
            posts_and_likes.append(templist)
        pagination = Paginator(posts_and_likes, 10)
        if pg_num == pagination.num_pages:
            last = True
        else:
            last = False
        follower_count = follower.objects.filter(followed = poster.id).count()
        following_count = follower.objects.filter(follower_id = poster.id).count()
        if str(request.user) == str(poster.username):
            followable = False
        else:
            followable = True
        try:
            test = follower.objects.get(followed = poster.id, follower_id = request.user.id )
            following = True
        except:
            following = False
        return render(request, "network/profile.html", {
            "poster":poster, "posts_and_likes":pagination.page(pg_num), "follower_count":follower_count, "follow_count":following_count, "followable":followable, "following":following, "pg_num":pg_num, "last": last
        })

def load_following(request, pg_num = 1):
    follow_list = follower.objects.filter(follower_id = request.user.id)
    id_list = []
    for i in follow_list:
        id_list.append(i.followed_id)
    posts = post.objects.filter(poster_id__in = id_list).order_by('-timestamp')
    posts_and_likes = []
    likes = []
    for i in range(len(posts)):
        likes.append(like.objects.filter(post_id = posts[i].id).count())
        templist = []
        templist.append(posts[i])
        templist.append(likes[i])
        posts_and_likes.append(templist)
    pagination = Paginator(posts_and_likes, 10)
    if pg_num == pagination.num_pages:
        last = True
    else:
        last = False
    return render(request, "network/following.html", {
        "posts_and_likes":pagination.page(pg_num), "pg_num":pg_num, "last": last
    })

def edit_post(request, post_id):
    currpost = post.objects.get(poster = request.user.id, id = post_id)
    currpost.text = request.body.decode("utf-8")[9:-2]
    currpost.save()
    return HttpResponse(status=204)


def like_post(request, post_id):
    print(request)
    print("user:", request.user.id)
    print(post_id)
    try:
        # verify liked post is not curruser's post
        test = post.objects.get(id = post_id, poster_id = request.user.id)
        print(test)
        return JsonResponse({
            "error": "User is attempting to like their own post."
        }, status=400)
    except:
        print("no post found")
    try:
        print("trying likes")
        like.objects.get(user_id = request.user.id, post_id = post_id)
        print("tried likes")
        return JsonResponse({
            "error": "User already liked this post."
        }, status = 400)
    except:
        print("creating like")
        liked = like.objects.create(user_id = request.user.id, post_id = post_id)
        print("created like")

    likes = like.objects.filter(post_id = post_id).count()
    print("no like found")
    print("likes:", likes)
    return JsonResponse(likes, safe=False)
    