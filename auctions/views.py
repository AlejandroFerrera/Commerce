
from urllib.request import Request
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from auctions.forms import ListingForm

from .models import Bid, Listing, User


def index(request):

    listings = Listing.objects.all()

    return render(request, "auctions/index.html", {'listings': listings})

def login_view(request):

    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)

            #Check if the user came from a protected route
            if 'next' in request.POST:
                nxt = request.POST.get("next")
                return redirect(nxt)

            return redirect("index")
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

@login_required
def add_listing(request):
    
    form = ListingForm()

    if request.method == "POST":
        data = ListingForm(request.POST)

        if data.is_valid():
            starting_bid = data.cleaned_data["starting_bid"]
            data = data.save(commit=False)
            
            data.price = starting_bid
            data.owner = request.user
            
            data.save()
            return redirect('index')
        else:
            return render(request, 'auctions/add-listing.html', {
                'form': form, 
                'message': 'Listing isn\'t valid'})

    return render(request, 'auctions/add-listing.html', {'form': form})

def listing(request, id):
   
    
    if request.method == "POST":

        action = request.POST.get("action")
        listing_id = request.POST.get("listing_id")
        listing = Listing.objects.get(id=listing_id)

        if action == 'add':
            request.user.watchlist.add(listing)
            return redirect('watchlist')
        elif action == 'remove':
            request.user.watchlist.remove(listing)
            return redirect('watchlist')
        elif action == 'bid':
            current_price = listing.price
            bid = int(request.POST.get("bid"))

            if bid <= current_price:
                messages.error(request, f"We're sorry, your bid must be greater than ${current_price}")
                return redirect('listing',id)
            
            #Updating the listing price
            listing.price = bid
            listing.save()
            #Saving the bid
            bid = Bid(user=request.user, listing=listing, amount=bid)
            bid.save()
            messages.success(request, "Bid succefully added")

            return redirect('listing', id)

    listing = Listing.objects.get(id=id)
    
    # Check if the user has the listing in his watchlist
    is_in_user_watchlist = False
    if request.user.is_authenticated:
        is_in_user_watchlist = True if request.user.watchlist.filter(id=id).count() == 1 else False
    
    last_bid = Bid.objects.filter(listing=listing).last()
    print(last_bid)
    
    return render(request, 'auctions/listing.html', {
        'listing': listing, 
        'is_in_user_watchlist': is_in_user_watchlist,
        'last_bid': last_bid})


def watchlist(request):
    user = request.user
    listings = user.watchlist.all()

    return render(request, 'auctions/watchlist.html', {'listings': listings})


