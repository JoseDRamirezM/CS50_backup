from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from urllib.parse import urlencode
from django.shortcuts import redirect


from .models import User, Listings, Bid, Comment


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listings.objects.all()
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
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return render(request, "auctions/index.html", {
        "listings": Listings.objects.all()
    })


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
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")

def add_listing(request):
    if request.method == "POST":
        
        #Parse all the attributes of the listing model
        title = request.POST["title"]
        description = request.POST["description"]
        price = request.POST["price"]
        img_url = request.POST["img_url"]
        category = request.POST["category"]
        creator_id = request.POST["creator_id"]

        #Check the mandatory fields
        if title and description and price != 0:
            try:
                listing = Listings(title = title, description = description,
                                price = price, img_url = img_url, category = category,
                                creator_id=creator_id)
                listing.save()
                return HttpResponseRedirect(reverse("auctions:index"))
            except IntegrityError:
                return render(request, "auctions/add_listing.html", {
                "message": "Check the entered data."
                })
        else: 
             return render(request, "auctions/add_listing.html", {
                "message": "Check the entered data."
            })
    else:
        return render(request, "auctions/add_listing.html")
        
def render_item(request, item_id, user_id, message):
    return render(request, "auctions/item.html", {
        "item" : Listings.objects.get(id=item_id), "watchlist": list(Listings.objects.filter(watchlist__id=user_id)),
        "message": message, "bids" : (list(Bid.objects.filter(listing__id=item_id))),
        "last": Bid.objects.all().last(), "comments": Comment.objects.filter(item__id=item_id)
    })

def render_item_not_auth(request, item_id):
    return render(request, "auctions/item.html", {
        "item" : Listings.objects.get(id=item_id)
    })


def add_watchlist(request, item_id, user_id):
    #add the user to the watchlist field of the listing object
    user = User.objects.get(id=int(user_id))
    item = Listings.objects.get(id=int(item_id))
    item.watchlist.add(user)
    return redirect('auctions:render_item', item_id=item_id, user_id=user_id, message="added")  

def remove_watchlist(request, item_id, user_id):
    #add the user to the watchlist field of the listing object
    user = User.objects.get(pk=int(user_id))
    item = Listings.objects.get(id=int(item_id))
    item.watchlist.remove(user)
    return redirect('auctions:render_item', item_id=item_id, user_id=user_id, message="removed")  

def place_bid(request, item_id, user_id):
    if request.method == "POST":
        bid = float(request.POST["bid"])
        item = Listings.objects.get(pk=item_id)
        user = User.objects.get(pk=user_id)

        #check if bid is greater than than any other or if it's at least as the starting bid 
        if bid >= item.price:
            #Check if it's the starting bid
            if not list(Bid.objects.filter(listing__id=item_id)):
                #create the bid
                item.price = bid
                item.save()
                actual_bid = Bid(value=bid, listing=item, bidder=user)
                actual_bid.save()
                return redirect('auctions:render_item', item_id=item_id, user_id=user_id, message="Success")
            else:
                if bid > item.price:
                    #check if the bid is valid when other bids had been placed
                    for b in list(Bid.objects.filter(listing__id=item_id)):
                        if bid < float(b.value):
                            return redirect('auctions:render_item', item_id=item_id, user_id=user_id,
                                message="Error placing the bid")
                    item.price = bid
                    item.save()
                    new_bid = Bid(value=bid, listing=item, bidder=user)
                    new_bid.save()
                    return redirect('auctions:render_item', item_id=item_id, user_id=user_id, message="Success")
                else:
                    return redirect('auctions:render_item', item_id=item_id, user_id=user_id, message="Bid must be greater than actual bid")
        else:
            return redirect('auctions:render_item', item_id=item_id, user_id=user_id,
                message="Error placing the bid")
    else: 
        return redirect('auctions:render_item', item_id=item_id, user_id=user_id,
                message="Error placing the bid")

def close_auction(request, user_id ,item_id):
    #update the is_active field of the Listing object to close the auction
    item = Listings.objects.get(id=item_id)
    item.is_active = False
    item.save()
    return redirect('auctions:render_item', item_id=item_id, user_id=user_id,
                message="Auction closed")

def add_comment(request, item_id, user_id):
    if request.method == "POST":
        comment_text = request.POST["comment"]
        item = Listings.objects.get(pk=item_id)
        user = User.objects.get(pk=user_id)
        
        if comment_text:
            comment = Comment(text=comment_text, author=user, item=item)
            comment.save()
            return redirect('auctions:render_item', item_id=item_id, user_id=user_id,
                message="Comment Published")
        else:
            return redirect('auctions:render_item', item_id=item_id, user_id=user_id,
                message="Error publishing comment")
    else:
        return redirect('auctions:render_item', item_id=item_id, user_id=user_id,
                message="Error publishing comment")

def render_watchlist(request, user_id):
    return render(request, "auctions/watchlist.html", {
        "items" : Listings.objects.filter(watchlist=user_id)
    })

def show_categories(request):
    return render(request, "auctions/categories.html", {
        "categories":  Listings.objects.order_by('category').values_list('category').distinct()
    })

def sort_by_category(request, category):
    return render(request, "auctions/index.html", {
        "listings": Listings.objects.filter(category=str(category))
    })