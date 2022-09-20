from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Bid, Comment, User, Category, Listing


class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "title", "starting_bid", "price", "active", "winner")
    filter_horizontal = ("watched",)

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id","user", "listing", "created", "text")

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "listing", "last_bided", "amount")

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Bid, BidAdmin)
