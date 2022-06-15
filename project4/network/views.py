from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
import json

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
        if content == "":
            messages.error(request, 'Blank post cannot be created')
            return HttpResponseRedirect(reverse("index"))

        user = request.user

        newpost = Newpost.objects.create(user=user, content=content)
        newpost.save()

        return HttpResponseRedirect(reverse("index"))

def profile(request, user_id):
    newpost = Newpost.objects.filter(user=user_id).order_by('-date')
    profile = User.objects.get(id=user_id)

    try:
        following = Follow.objects.get(user=request.user, profile=user_id)
        follow = following.follow
    except:
        follow = False
    
    try:
        followingcount = len(Follow.objects.filter(user=user_id, follow=True))
        followercount = len(Follow.objects.filter(profile=user_id, follow=True))
    except:
        followercount = 0
        followingcount = 0

    
    return render(request,  "network/profile.html", {
        "newpost": newpost,
        "profile": profile,
        "followercount": followercount,
        "followingcount": followingcount,
        "is_following": follow

    })

def follow(request, user_id):
    user = request.user
    profile = User.objects.get(id=user_id)

    if request.method == "PUT":
        data = json.loads(request.body)
        try:
            follow = Follow.objects.get(user=user, profile=profile)
            follow.follow = data.get("follow")
            follow.save()
        except:
            follow = Follow.objects.create(user=user, profile=profile, follow=True)
            follow.save()

        return HttpResponse(status=204)

    if request.method == "GET":

        try:
            followingcount = len(Follow.objects.filter(user=user_id, follow=True))
            followercount = len(Follow.objects.filter(profile=user_id, follow=True))
        except:
            followercount = 0
            followingcount = 0

        followcount = {
            "followercount" : followercount,
        }
        return JsonResponse(followcount) 
    