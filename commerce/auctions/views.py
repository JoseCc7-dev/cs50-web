import sqlite3
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, listings, comments, watchlist

def index(request):
    if request.method == "POST":
        conn = sqlite3.connect('db.sqlite3')
        c = conn.cursor()
        name = request.user
        temp = User.objects.get(username = name)
        title = request.POST["title"]
        category = request.POST["category"].capitalize()
        description = request.POST["description"]
        if request.POST["image_url"]:     
            imageurl = request.POST["image_url"]
        else:
            imageurl = ""
        starting_bid = request.POST["starting_bid"]
        c.execute("INSERT INTO auctions_listings(title, creator_id, category, description, imageurl, starting_bid) VALUES(?, ?, ?, ?, ?, ?)", (title, temp.id, category, description, imageurl, starting_bid))
        conn.commit()
        c.close()
        return render(request, "auctions/index.html", {
            "listings": listings.objects.all()
        })
    else:
        listing = listings.objects.all()
        return render(request, "auctions/index.html", {
            "listings": listing
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def new_listing(request):
    return render(request, "auctions/addListing.html")

def load(request, listing):
    if request.method == "POST":
        # Update current bid
        if request.POST.get("bid"):
            return placebid(request, listing)
        # Close listing
        elif request.POST.get("close"):
            return closelisting(request, listing)
        elif request.POST.get("add_comment"):
            return addcomment(request, listing)
        # Remove/add listing from/to watchlist
        else:
            return editwatchlist(request, listing)
    # if request == get
    else:
        data = listings.objects.get(title= listing)
        entry = data.description.split('\n')
        content = []
        for i in range(0, len(entry)):
            if i < len(entry)-1:
                word = entry[i]
                temp = word
                content.append(temp)
            else:
                content.append(entry[i])
        name = request.user
        try: 
            winner_id = data.winner_id
            winner_name = User.objects.get(id = winner_id)
            if str(winner_name.username) == str(name):
                winner = True
            else:
                winner = None
        except:
            winner = None
        # if user not authenticated?
        try:
            id = User.objects.get(username = name).id
        except:
            return render(request, "auctions/load.html", {
            "item":data, "content":content, "winner":winner
        })
        creator = None
        if id == data.creator_id:
            creator = True
        try:
            comment = []
            comment.append(comments.objects.get(listing_id = data.id))
        except:
            comment = comments.objects.filter(listing_id = data.id)
        for i, s in enumerate(comment):
            comment[i].user_id = (User.objects.get(id = s.user_id)).username.capitalize()
        # if listing not in user's watchlist
        try:
            check = watchlist.objects.get(listing_id = data.id)
        except:
            return render(request, "auctions/load.html", {
            "item":data, "content":content, "creator":creator, "winner":winner, "comments":comment
        })
        else:
            return render(request, "auctions/load.html", {
            "item":data, "content":content, "added":"yes", "creator":creator, "winner":winner, "comments":comment
        })

def loadwatchlist(request):
    user = request.user
    id = User.objects.get(username = user).id
    data = watchlist.objects.filter(user_id =  id)
    list = []
    for i in data:
        temp = listings.objects.get(id = i.listing_id)
        list.append(temp.title)
    return render(request, "auctions/watchlist.html", {
        "listings":list
    })

def loadcategories(request):
    if request.method == "POST":
        category = request.POST.get("cat")
        data = listings.objects.filter(category= category)
        listing = set()
        for i in data:
            temp = i.title.capitalize()
            listing.add(temp)
        return render(request, "auctions/categories.html", {
            "listings":data
        })
    else:  
        data = listings.objects.filter()
        cats = set()
        for i in data:
            temp = i.category
            cats.add(temp)
        return render(request, "auctions/categories.html", {
            "cats":cats
        })

def editwatchlist(request, listing):
    name = request.user
    temp = User.objects.get(username = name)
    id = temp.id
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    data = listings.objects.get(title= listing)
    try: 
        winner_id = data.winner_id
        winner_name = User.objects.get(id = winner_id)
        if str(winner_name.username) == str(name):
            winner = True
        else:
            winner = None
    except:
        winner = None
    creator = None
    if id == data.creator_id:
        creator = True
    try:
        comment = []
        comment.append(comments.objects.get(listing_id = data.id))
    except:
        comment = comments.objects.filter(listing_id = data.id)
    for i, s in enumerate(comment):
        comment[i].user_id = (User.objects.get(id = s.user_id)).username.capitalize()
    entry = data.description.split('\n')
    content = []
    for i in range(0, len(entry)):
        if i < len(entry)-1:
            word = entry[i]
            temp = word[:-1]
            content.append(temp)
        else:
            content.append(entry[i])
    try:
        check = watchlist.objects.get(listing_id = data.id)
    except:
        check = 0
    if request.POST.get("remove"):
        sql = "DELETE FROM auctions_watchlist WHERE id = ?"
        c.execute(sql, (check.id,))
        conn.commit()
        c.close()
        return render(request, "auctions/load.html", {
        "item":data, "content":content, "winner":winner, "creator":creator, "comments":comment
        })
    elif request.POST.get("add"):
        c.execute("INSERT INTO auctions_watchlist(user_id, listing_id) VALUES(?, ?)", (id, data.id))
        conn.commit()
        c.close()
        return render(request, "auctions/load.html", {
        "item":data, "content":content, "added":"yes", "winner":winner, "creator":creator, "comments":comment
        })  

def closelisting(request,listing):
    name = request.user
    temp = User.objects.get(username = name)
    id = temp.id
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    data = listings.objects.get(title= listing)
    try: 
        winner_id = data.winner_id
        winner_name = User.objects.get(id = winner_id)
        if str(winner_name.username) == str(name):
            winner = True
        else:
            winner = None
    except:
        winner = None
    creator = None
    if id == data.creator_id:
        creator = True
    try:
        comment = []
        comment.append(comments.objects.get(listing_id = data.id))
    except:
        comment = comments.objects.filter(listing_id = data.id)
    for i, s in enumerate(comment):
        comment[i].user_id = (User.objects.get(id = s.user_id)).username.capitalize()
    entry = data.description.split('\n')
    content = []
    for i in range(0, len(entry)):
        if i < len(entry)-1:
            word = entry[i]
            temp = word[:-1]
            content.append(temp)
        else:
            content.append(entry[i])
    try:
        check = watchlist.objects.get(listing_id = data.id)
    except:
        check = 0
    sql = "UPDATE auctions_listings SET active = False WHERE id = ?"
    c.execute(sql, (data.id,))
    conn.commit()
    c.close()
    if check == 0:
        return render(request, "auctions/load.html",{
        "item":data, "content":content, "winner":winner, "creator":creator, "comments":comment
        })
    elif check:
        return render(request, "auctions/load.html",{
        "item":data, "content":content, "added":"yes", "winner":winner, "creator":creator, "comments":comment
        })

def placebid(request, listing):
    name = request.user
    temp = User.objects.get(username = name)
    id = temp.id
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    data = listings.objects.get(title= listing)
    try: 
        winner_id = data.winner_id
        winner_name = User.objects.get(id = winner_id)
        if str(winner_name.username) == str(name):
            winner = True
        else:
            winner = None
    except:
        winner = None
    creator = None
    if id == data.creator_id:
        creator = True
    try:
        comment = []
        comment.append(comments.objects.get(listing_id = data.id))
    except:
        comment = comments.objects.filter(listing_id = data.id)
    for i, s in enumerate(comment):
        comment[i].user_id = (User.objects.get(id = s.user_id)).username.capitalize()
    try:
        check = watchlist.objects.get(listing_id = data.id)
    except:
        check = 0
    bid = int(request.POST.get("bid"))
    if bid <= data.current_bid:
        return HttpResponse("Invalid Bid, Must Be Greater Than Current Bid")
    else:
        sql = "UPDATE auctions_listings SET current_bid = ?, winner_id = ? WHERE id = ?"
        c.execute(sql, (bid, id, data.id,))
        conn.commit()
        c.close()
        data = listings.objects.get(title= listing)
        entry = data.description.split('\n')
        content = []
        for i in range(0, len(entry)):
            if i < len(entry)-1:
                word = entry[i]
                temp = word[:-1]
                content.append(temp)
            else:
                content.append(entry[i])
        if check == 0:
            return render(request, "auctions/load.html",{
            "item":data, "content":content, "creator":creator, "winner":winner, "comments":comment
            })
        elif check:
            return render(request, "auctions/load.html",{
            "item":data, "content":content, "added":"yes", "creator":creator, "winner":winner, "comments":comment
            })

def addcomment(request, listing):
    name = request.user
    temp = User.objects.get(username = name)
    id = temp.id
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    data = listings.objects.get(title= listing)
    try: 
        winner_id = data.winner_id
        winner_name = User.objects.get(id = winner_id)
        if str(winner_name.username) == str(name):
            winner = True
        else:
            winner = None
    except:
        winner = None
    creator = None
    if id == data.creator_id:
        creator = True
    entry = data.description.split('\n')
    content = []
    for i in range(0, len(entry)):
        if i < len(entry)-1:
            word = entry[i]
            temp = word[:-1]
            content.append(temp)
        else:
            content.append(entry[i])
    try:
        check = watchlist.objects.get(listing_id = data.id)
    except:
        check = 0
    text = request.POST.get("comment")
    print(text)
    sql = "INSERT INTO auctions_comments(user_id, listing_id, text) VALUES(?, ?, ?)"
    c.execute(sql, (id, data.id, text,))
    conn.commit()
    c.close()
    try:
        comment = []
        comment.append(comments.objects.get(listing_id = data.id))
    except:
        comment = comments.objects.filter(listing_id = data.id)
    for i, s in enumerate(comment):
        comment[i].user_id = (User.objects.get(id = s.user_id)).username.capitalize()
    if check == 0:
        return render(request, "auctions/load.html",{
        "item":data, "content":content, "creator":creator, "winner":winner, "comments":comment
        })
    elif check:
        return render(request, "auctions/load.html",{
        "item":data, "content":content, "added":"yes", "creator":creator, "winner":winner, "comments":comment
        })