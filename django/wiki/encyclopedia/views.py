from django.shortcuts import render
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from markdown2 import Markdown
from . import util
from random import choices


class NewForm(forms.Form):
    forms = forms.CharField(label='', 
                    widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))

markdowner = Markdown()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(), 
        "form": NewForm
    })

def wiki(request, title):
    if not util.get_entry(title):
        return render(request, "encyclopedia/error.html", {
                "message": "Content not available"
            })
    else:
        md = util.get_entry(title)
        data = markdowner.convert(md)
        return render(request, "encyclopedia/entry.html", {
            "data": data, "form": NewForm, "title": title
        })

def search(request):
    if request.method == "POST":
        form = NewForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["forms"]

    
    if util.get_entry(title):
        return HttpResponseRedirect(f'wiki/{title}')


    possible_entry = []
    for entry in util.list_entries():
        if title.lower() in entry.lower():
            possible_entry.append(entry)
    return render(request, "encyclopedia/search.html", {
        "entries": possible_entry, 
        "form": NewForm
    })

def newpage(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if util.get_entry(title) != None:
            return render(request, "encyclopedia/error.html", {
                "message": "Page already exists"
            })
        else:
            util.save_entry(title, content)
            return HttpResponseRedirect(f'/wiki/{title}')

    else:
        return render(request, "encyclopedia/newpage.html")

def editpage(request, title):

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        util.save_entry(title, content)
        return HttpResponseRedirect(f'/wiki/{title}')

    else:
        content = util.get_entry(title)
        return render(request, "encyclopedia/editpage.html", {
            "title": title,
            "content": content
        })

def random(request):
    list_of_titles = util.list_entries()
    title = choices(list_of_titles)[0]
    return HttpResponseRedirect(f'/wiki/{title}')