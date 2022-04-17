from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, title):
    if not util.get_entry(title):
        return render(request, "encyclopedia/error.html")
    else:
        data = util.get_entry(title)
        return render(request, "encyclopedia/entry.html", {
            "data": data
        })

