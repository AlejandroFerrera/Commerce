from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add-listing", views.add_listing, name="add-listing"),
    path("listing/<str:id>", views.listing, name='listing'),
    path("watchlist/", views.watchlist, name="watchlist"),
    path('categories', views.categories, name='categories'),
    path('category/<str:id>', views.category, name='category')
]
