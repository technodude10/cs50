from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("<int:listing_id>/listing_page", views.listing_page, name="listing_page"),
    path("<int:listing_id>/place_bid", views.place_bid, name="place_bid"),
    path("<int:listing_id>/watchlist", views.watchlist, name="watchlist"),
    path("<int:listing_id>/close", views.close, name="close"),
    path("<int:listing_id>/comments", views.comments, name="comments"),
    path("watchlist_view", views.watchlist_view, name="watchlist_view"),
    path("categories", views.categories, name="categories"),
    path("<str:categoryvalue>/category", views.category, name="category")
]