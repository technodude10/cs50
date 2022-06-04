from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Watchlist


def index(request):
    listing = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listing": listing
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

def create_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        desc = request.POST["desc"]
        bid = request.POST["bid"]
        url = request.POST["url"]
        category = request.POST["category"]
        userid = request.user
        listing = Listing.objects.create(title=title, desc=desc, bid=bid, url=url, category=category, userid=userid)
        listing.save()
        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "auctions/create_listing.html")


def listing_page(request, listing_id):
    list = Listing.objects.get(pk=listing_id)
    return render(request, "auctions/listing_page.html", {
        "list": list,
        "in_wishlist": in_wishlist(request, listing_id)
    })

def place_bid(request, listing_id):
    if request.method == "POST":
        bid_value = request.POST["bid_value"]
        list = Listing.objects.get(pk=listing_id)
        print(bid_value, list)
        
        return HttpResponseRedirect("listing_page")


def in_wishlist(request, listing_id):
    try:
        user = request.user
        list = Listing.objects.get(pk=listing_id)
        watchlist =  Watchlist.objects.filter(userwatchlist=user, listwatchlist=list).first()
        if watchlist == None:
            return False
        else:
            return True
    except:
        return None

@login_required
def watchlist(request, listing_id):
    userwatchlist = request.user
    listwatchlist = Listing.objects.get(pk=listing_id)

    if not in_wishlist(request, listing_id):
        watchlist = Watchlist.objects.create(userwatchlist=userwatchlist, listwatchlist=listwatchlist)
        watchlist.save
        return HttpResponseRedirect("listing_page")
    else:
        watchlist =  Watchlist.objects.filter(userwatchlist=userwatchlist, listwatchlist=listwatchlist).delete()
        return HttpResponseRedirect("listing_page")

        
    
    
        