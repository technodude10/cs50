from typing import List
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Watchlist, Bid, Comments



categorylist = ['electronics', 'art', 'toys', 'fashion']

def index(request):
    listing = Listing.objects.filter(open_or_close = True)
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
        user = request.user
        listing = Listing.objects.create(title=title, desc=desc, bid=bid, url=url, category=category, user=user)
        listing.save()
        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "auctions/create_listing.html", {
            "categories" : categorylist 
        })



def listing_page(request, listing_id):
    list = Listing.objects.get(pk=listing_id)
    bid = Bid.objects.filter(list=list).order_by('-bid_value')
    bidlen = len(bid)

    # current higgest bidder
    try:
        if request.user == bid.first().user:
            messages.info(request, 'Your bid is the current bid')
    except:
        pass

    # if the creator has closed or not > only for creators
    if if_creator(request, listing_id) and list.open_or_close:
        creatorclosed = True
    else:
        creatorclosed = False

    #Winner
    winner = None
    try:
        if request.user == bid.first().user:
            winner = bid.first().user
    except:
        pass

    #comment
    comments = Comments.objects.filter(list=list)

    return render(request, "auctions/listing_page.html", {
        "list": list,
        "in_wishlist": in_wishlist(request, listing_id),
        "creatorclosed": creatorclosed,
        "listopen_or_close": list.open_or_close,
        "bidlen": bidlen,
        "winner": winner,
        "comments": comments
    })

@login_required
def place_bid(request, listing_id):
    if request.method == "POST":
        user = request.user
        try:
            bid_value = float(request.POST["bid_value"])
        except:
            bid_value = 0

        list = Listing.objects.get(pk=listing_id)

        if bid_value > list.bid:
            list.bid = bid_value
            list.save()

            try:
                bid = Bid.objects.get(user=user, list=list)
            except:
                bid = None

            if bid == None:
                bid = Bid.objects.create(user=user, list=list, bid_value=bid_value)
            else:
                bid.bid_value = bid_value
                bid.save()
                
            return HttpResponseRedirect("listing_page")

        else:
            messages.error(request, 'Your bid is lower than current bid')
            return HttpResponseRedirect("listing_page") 


def in_wishlist(request, listing_id): # not a view
    try:
        user = request.user
        list = Listing.objects.get(pk=listing_id)
        watchlist =  Watchlist.objects.filter(user=user, list=list).first()
        if watchlist == None:
            return False
        else:
            return True
    except:
        return None

@login_required
def watchlist(request, listing_id):
    user = request.user
    list = Listing.objects.get(pk=listing_id)

    if not in_wishlist(request, listing_id):
        watchlist = Watchlist.objects.create(user=user, list=list)
        watchlist.save
        return HttpResponseRedirect("listing_page")
    else:
        watchlist =  Watchlist.objects.filter(user=user, list=list).delete()
        return HttpResponseRedirect("listing_page")

@login_required
def close(request, listing_id):
    user = request.user
    list = Listing.objects.get(pk=listing_id, user=user, open_or_close=True)
    list.open_or_close = False
    list.save()
    return redirect("index")

        
def if_creator(request, listing_id):
    user = request.user
    list = Listing.objects.get(pk=listing_id)
    if list.user == user:
        return True
    else:
        return None

    
    
def comments(request, listing_id):
     if request.method == "POST":
        comment = request.POST["comment"]
        user = request.user
        list = Listing.objects.get(pk=listing_id)
        comments = Comments.objects.create(user=user, list=list, comment=comment)
        comments.save()
        return HttpResponseRedirect("listing_page")      

@login_required
def watchlist_view(request):
    user = request.user
    watchlist = Watchlist.objects.filter(user=user)
    return render(request, "auctions/watchlist.html", {
        "watchlists": watchlist
    })

def categories(request):
    return render(request, "auctions/categories.html", {
        "categorylist": categorylist
        })
    

@login_required
def category(request, categoryvalue):
    categoryobj = Listing.objects.filter(category=categoryvalue)
    print(categoryobj)
    return render(request, "auctions/categorylisting.html", {
        "categoryobj": categoryobj,
        "categoryvalue": categoryvalue
    })