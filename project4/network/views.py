from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
import json
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Follow, User, Newpost

# index views display all post in chronological order
def index(request):
    """ In this view pagination is used to display only 10 posts per page """
    newpost = Newpost.objects.all().order_by('-date')
    paginator = Paginator(newpost, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {
        "newpost": page_obj,
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

# this view lets users create a new text post and stores inside database
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

# profile view shows each individuals profile details and posts
def profile(request, user_id):
    newpost = Newpost.objects.filter(user=user_id).order_by('-date')
    profile = User.objects.get(id=user_id)
    paginator = Paginator(newpost, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

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

    
    return render(request,  "network/index.html", {
        "newpost": page_obj,
        "profile": profile,
        "followercount": followercount,
        "followingcount": followingcount,
        "is_following": follow,
        "is_profilepage": True

    })

# Follow view lets users follow/unfollow other profiles async
@login_required
def follow(request, user_id):
    user = request.user
    profile = User.objects.get(id=user_id)
    """ gets data from js to follow/unfollow"""
    if request.method == "PUT":
        data = json.loads(request.body)
        try:
            follow = Follow.objects.get(user=user, profile=profile)
            follow.follow = data.get("follow")
            follow.save()
        except:
            follow = Follow.objects.create(user=user, profile=profile, follow=True)
            follow.save()

        return JsonResponse({"message": "changes received."}, status=201)

# this view uses
@login_required
def following_page(request):
    user = request.user
    follow = Follow.objects.filter(user=user, follow=True)
    
    # make sure that the follow object is not null
    if not follow:
        page_obj = None
    else:
        # gets the post of all the following users using Q object
        query = Q()
        for profile in follow:
            query = query | Q(user = profile.profile)

        #get posts followed by the user
        followpost = Newpost.objects.filter(query).order_by('-date')
        paginator = Paginator(followpost, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    

    # return HttpResponseRedirect(reverse("index"))
    return render(request, "network/index.html", {
        "newpost": page_obj,
        "followpage": True
    })

# edit already created post using js and api
@login_required
def editpost(request, post_id):

    if request.method == "POST":
        data = json.loads(request.body)

        id = data.get("id")
        content = data.get("content")

        if content == "":
            return JsonResponse({"message": "error"}, status=400)
            

        editpost = Newpost.objects.get(id=id)
        editpost.content = content
        editpost.save()
        
        return JsonResponse({"message": "changes received."}, status=201)

    editpost = Newpost.objects.get(id = post_id )
    return JsonResponse(editpost.serialize())

# update follower count async
@login_required
def updatefollow(request, user_id):

    try:
        followercount = len(Follow.objects.filter(profile=user_id, follow=True))
    except:
        followercount = 0

    return JsonResponse({"followercount": followercount}, status=201)

# update like/unlike async
@login_required
def like(request, post_id):

    if request.method == "PUT":
        data = json.loads(request.body)

        likes = Newpost.objects.filter(id=post_id)
        if not likes.exists():
            return JsonResponse({}, status=400)
        obj = likes.first()
        if request.user in obj.like.all():
            obj.like.remove(request.user)
            liked = False
        else:
            obj.like.add(request.user)
            liked = True
        return JsonResponse({"like": liked}, status=201)
        
    likes = Newpost.objects.get(id=post_id)
    likecount = len(likes.like.all())
    return JsonResponse({"likecount": likecount}, status=201)