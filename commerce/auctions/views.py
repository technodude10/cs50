from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# imports models from models.py
from .models import User, Listing, Watchlist, Bid, Comments 


# a list of all categories in sorted list
categorylist = ['electronics', 'art', 'toys', 'fashion']
categorylist.sort()

# index page -> displays all the active listings
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

# create a listing
def create_listing(request):
    if request.method == "POST":

        # checks if neccessary fields are filled or not
        title = request.POST["title"]
        if title == '':
            messages.error(request, 'Enter a title for the listing')
            return render(request, "auctions/create_listing.html", {
            "categories" : categorylist 
        })

        desc = request.POST["desc"]
        if desc == '':
            messages.error(request, 'Enter a description for the listing')
            return render(request, "auctions/create_listing.html", {
            "categories" : categorylist 
        })

        bid = request.POST["bid"]

        if bid == '':
            messages.error(request, 'Enter a bid for the listing')
            return render(request, "auctions/create_listing.html", {
            "categories" : categorylist 
        })

        url = request.POST["url"]
        if url == '':
            messages.error(request, 'Enter a image url for the listing')
            return render(request, "auctions/create_listing.html", {
            "categories" : categorylist 
        })

        category = request.POST["category"]

        # get currently logged user details
        user = request.user

        # saves listing to listing database
        listing = Listing.objects.create(title=title, desc=desc, bid=bid, url=url, category=category, user=user)
        listing.save()
        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "auctions/create_listing.html", {
            "categories" : categorylist 
        })


# In detail listing of each listings
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

# Collects the bid entered by the user and performs validation before adding to database
@login_required
def place_bid(request, listing_id):
    if request.method == "POST":
        user = request.user

        # gets bid value, if no bid is given try except is used to pass 0 as the bid value
        try:
            bid_value = float(request.POST["bid_value"])
        except:
            bid_value = 0

        # get listing details of specific listing based on its listing id
        list = Listing.objects.get(pk=listing_id)

        # checks if bid value is larger than current value
        if bid_value > list.bid:
            list.bid = bid_value
            list.save()

            try:
                bid = Bid.objects.get(user=user, list=list)
            except:
                bid = None

            # creates a new bid database listing or updates existing ones
            if bid == None:
                bid = Bid.objects.create(user=user, list=list, bid_value=bid_value)
            else:
                bid.bid_value = bid_value
                bid.save()
                
            return HttpResponseRedirect("listing_page")

        else:
            # messages to notify the user 
            messages.error(request, 'Your bid is lower than current bid')
            return HttpResponseRedirect("listing_page") 


# a funtion to determine if a listing is watchlisted by the user or not
def in_wishlist(request, listing_id): 
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

# allows user to add/remove a listing from watchlist
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

# allows the creator of a listing to close it and thus declaring the highest bidder the winner
@login_required
def close(request, listing_id):
    user = request.user
    list = Listing.objects.get(pk=listing_id, user=user, open_or_close=True)
    list.open_or_close = False
    list.save()
    return redirect("index")

# a funtion to check if the list is created by the logged in user or not        
def if_creator(request, listing_id):
    user = request.user
    list = Listing.objects.get(pk=listing_id)
    if list.user == user:
        return True
    else:
        return None

# allows user to comment on listings   
@login_required    
def comments(request, listing_id):
     if request.method == "POST":
        comment = request.POST["comment"]
        user = request.user
        list = Listing.objects.get(pk=listing_id)
        comments = Comments.objects.create(user=user, list=list, comment=comment)
        comments.save()
        return HttpResponseRedirect("listing_page")      

# a page that lists all the watchlisted items
@login_required
def watchlist_view(request):
    user = request.user
    watchlist = Watchlist.objects.filter(user=user)
    return render(request, "auctions/watchlist.html", {
        "watchlists": watchlist
    })

# a page that displays all the different categories as links
@login_required
def categories(request):
    return render(request, "auctions/categories.html", {
        "categorylist": categorylist
        })
    
# a page that lists all the listings that come under a specific category
@login_required
def category(request, categoryvalue):
    categoryobj = Listing.objects.filter(category=categoryvalue)
    return render(request, "auctions/categorylisting.html", {
        "categoryobj": categoryobj,
        "categoryvalue": categoryvalue
    })