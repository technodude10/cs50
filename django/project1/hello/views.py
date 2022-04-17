from importlib import import_module
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Hello!")

def annlee(request):
    return HttpResponse("Hello, Annlee")

def david(request):
    return HttpResponse("Hello, David")

def greet(request, name):
    return HttpResponse(f"Hello, {name.capitalize()}")
