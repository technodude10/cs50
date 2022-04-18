from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util

class NewForm(forms.Form):
    forms = forms.CharField(label='', 
                    widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(), 
        "form": NewForm
    })

def wiki(request, title):
    if not util.get_entry(title):
        return render(request, "encyclopedia/error.html")
    else:
        data = util.get_entry(title)
        return render(request, "encyclopedia/entry.html", {
            "data": data, "form": NewForm
        })

def search(request):
    if request.method == "POST":
        form = NewForm(request.POST)
        if form.is_valid():
            forms = form.cleaned_data["forms"]
            
    if util.get_entry(forms):
        data = util.get_entry(forms)
        return render(request, "encyclopedia/entry.html", {
            "data": data, "form": NewForm
        })

    possible_entry = []
    for entry in util.list_entries():
        if forms.lower() in entry.lower():
            possible_entry.append(entry)
    return render(request, "encyclopedia/search.html", {
        "entries": possible_entry, 
        "form": NewForm
    })
