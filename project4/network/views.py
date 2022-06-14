from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Follow, User, Newpost


def index(request):
    newpost = Newpost.objects.all().order_by('-date')
    return render(request, "network/index.html", {
        "newpost": newpost
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

@login_required 
def newpost(request):
    if request.method == "POST":
        content = request.POST["content"]

        user = request.user

        newpost = Newpost.objects.create(user=user, content=content)
        newpost.save()

        return HttpResponseRedirect(reverse("index"))

def profile(request, user_id):
    newpost = Newpost.objects.filter(user=user_id).order_by('-date')
    user = User.objects.get(id=user_id)
    try:
        follow = Follow.objects.get(user=user_id)
        followercount = len(follow.follower.all())
        followingcount = len(follow.following.all())
    except:
        followercount = 0
        followingcount = 0
    
    return render(request, "network/profile.html", {
        "newpost": newpost,
        "profile": user,
        "followercount": followercount,
        "followingcount": followingcount
    })