from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Bid, Listing


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