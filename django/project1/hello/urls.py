from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("annlee", views.annlee, name="brian"),
    path("david", views.david, name="david"),
    path("<str:name>", views.greet, name="greet")
]