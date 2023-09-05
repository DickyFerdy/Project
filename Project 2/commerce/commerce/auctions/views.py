from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Bid, Listing, Transaction, Comments


def index(request):
    listing_data = Listing.objects.filter(isActive=True)
    return render(request, "auctions/index.html", {
        "listings": listing_data
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
    categories = Category.objects.all()
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']
        image = request.POST['imageUrl']
        price = request.POST['price']
        category = request.POST['category']
        user = request.user

        categoryData = Category.objects.get(categoryName=category)
        
        listing_data = Listing(title=title,
                              description=description,
                              imageURL=image,
                              price=price,
                              category=categoryData,
                              owner=user)
        listing_data.save()
        return HttpResponseRedirect(reverse("index"))
    else:    
        return render(request, "auctions/create_listing.html", {
            "categories": categories
        })
        
        
def categories(request):
    categories = Category.objects.all()
    list_category = []

    for category in categories:
        active_listing = Listing.objects.filter(isActive=True, category=category)
        count_listing = active_listing.count()
        list_category.append({
            "category": category,
            "count_listing": count_listing
        })
    
    return render(request, "auctions/categories.html", {
        "list_category": list_category
    })
    
    
def category_view(request, id):
    category_data = Category.objects.get(pk=id)
    listing_data = Listing.objects.filter(isActive=True, category=category_data)
    return render(request, "auctions/category_view.html", {
        "listings": listing_data,
        "category": category_data
    })
    
    
def listing(request, id):
    listing_data = Listing.objects.get(pk=id)
    category = Category.objects.get(categoryName=listing_data.category)
    owner = User.objects.get(username=listing_data.owner)
    comments = Comments.objects.filter(listing=listing_data)
    watchlist = request.user in listing_data.watchlist.all()
    return render(request, "auctions/listing.html", {
        "listing": listing_data,
        "category": category,
        "owner": owner,
        "comments": comments,
        "watchlist": watchlist
    })
    
    
def listed_by(request, id):
    owner = User.objects.get(pk=id)
    listings = Listing.objects.filter(owner=owner)
    return render(request, "auctions/listed_by.html", {
        "owner": owner,
        "listings": listings
    })
    
    
def new_bid(request, id):
    listing_data = Listing.objects.get(pk=id)
    category = Category.objects.get(categoryName=listing_data.category)
    owner = User.objects.get(username=listing_data.owner)
    user = request.user
    if request.method == "POST":
        newBid = float(request.POST['bid'])
        if listing_data.bidPrice is None:
            if newBid > listing_data.price:
                update_bid = Bid(user=user, bid=newBid)
                update_bid.save()
                listing_data.bidPrice = update_bid
                listing_data.save()
                
                transaction = Transaction(user=user,
                                          listing=listing_data,
                                          bid=update_bid)
                transaction.save()

                return render(request, "auctions/listing.html", {
                    "listing": listing_data,
                    "success": "Your bid was succesfully added",
                    "category": category,
                    "owner": owner
                })
            else:
                return render(request, "auctions/listing.html", {
                    "listing": listing_data,
                    "error": "Your bid must be higher than the current price.",
                    "category": category,
                    "owner": owner
                })
        else:
            if newBid > listing_data.bidPrice.bid:
                update_bid = Bid(user=user, bid=newBid)
                update_bid.save()
                listing_data.bidPrice = update_bid
                listing_data.save()

                transaction = Transaction(user=user,
                            listing=listing_data,
                            bid=update_bid)
                transaction.save()
                
                return render(request, "auctions/listing.html", {
                    "listing": listing_data,
                    "success": "Your bid was succesfully added",
                    "category": category,
                    "owner": owner
                })
            else:
                return render(request, "auctions/listing.html", {
                    "listing": listing_data,
                    "error": "Your bid must be higher than the current price.",
                    "category": category,
                    "owner": owner
                })
    else:
        return render(request, "auctions/listing.html", {
            "listing": listing_data,
            "category": category,
            "owner": owner
        })
        
        
def my_listing(request):
     user = request.user
     listing_data = Listing.objects.filter(owner=user)
     return render(request, "auctions/my_listing.html", {
         "listings": listing_data
     })


def transaction(request):
    user = request.user
    user_transaction = Transaction.objects.filter(user=user)
    listings = set()

    for transaction in user_transaction:
        listings.add(transaction.listing)
        
    return render(request, "auctions/transaction.html", {
        "listings": listings
    }) 
 
        
def comment(request, id):
    listing_data = Listing.objects.get(pk=id)
    user = request.user
    message = request.POST['newComment']
    
    comment = Comments(author=user,
                       listing=listing_data,
                       message=message)
    comment.save()

    return HttpResponseRedirect(reverse("listing", args=(id, )))


def close_auction(request, id):
    listing_data = Listing.objects.get(pk=id)
    listing_data.isActive = False
    listing_data.save()
    category = Category.objects.get(categoryName=listing_data.category)
    owner = User.objects.get(username=listing_data.owner)
    watchlist = request.user in listing_data.watchlist.all()
    comments = Comments.objects.filter(listing=listing_data)
    
    return render(request, "auctions/listing.html", {
        "listing": listing_data,
        "category": category,
        "owner": owner,
        "comments": comments,
        "watchlist": watchlist
    })
    

def watchlist_display(request):
    user = request.user
    listings = user.listing_watchlist.all()
    
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })
    
    
def watchlist_add(request, id):
    listing_data = Listing.objects.get(pk=id)
    user = request.user
    listing_data.watchlist.add(user)

    return HttpResponseRedirect(reverse("listing", args=(id, )))
    
    
def watchlist_remove(request, id):
    listing_data = Listing.objects.get(pk=id)
    user = request.user
    listing_data.watchlist.remove(user)

    return HttpResponseRedirect(reverse("listing", args=(id, )))