
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.newpost, name="newpost"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("following_page", views.following_page, name="following_page"),
    

     # API Routes
     path("follow/<int:user_id>", views.follow, name="follow"),
     path("editpost/<int:post_id>", views.editpost, name="editpost"),
     path("updatefollow/<int:user_id>", views.updatefollow, name="updatefollow")


]

