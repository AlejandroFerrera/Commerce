
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass
    # The user's watchlist is created in listing model with a many to many relation between listing and user.
    # This user model has default fields from Django Abstract User (username, password, etc). 

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.id}: {self.name}"

class Listing(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=700, blank=True)
    starting_bid = models.DecimalField(max_digits=9, decimal_places=2)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    image_url = models.URLField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="wins")
    watched = models.ManyToManyField(User, related_name="watchlist", blank=True) #Watchlist

    def __str__(self):
        return f"{self.title} ${self.price}"


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    last_bided = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}: {self.user} on {self.listing} at {self.last_bided} bids: ${self.amount}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    text = models.CharField(max_length=700)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} on {self.listing} at {self.created}: \n {self.text}"

