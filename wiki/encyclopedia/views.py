from django.shortcuts import render, redirect

from . import util

import markdown2

from django import forms

import random

#from django.http import HttpResponse

#def test_entry(request, title):
    #return HttpResponse(f"Title received: {title}")

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea, label="Content")

def entry(request, title):
    content = util.get_entry(title)
    if content:
        html_content = markdown2.markdown(content)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })
    return render(request, "encyclopedia/error.html", {
        "message": f"The entry '{title}' was not found."
    })

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def search(request):
    query = request.GET.get("q", "")
    entries = util.list_entries()

    # Exact match → redirect
    if query in entries:
        return redirect("entry", title=query)

    # Substring match → show results
    results = [entry for entry in entries if query.lower() in entry.lower()]
    return render(request, "encyclopedia/search.html", {
        "query": query,
        "results": results
    })


def create(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            if util.get_entry(title):
                return render(request, "encyclopedia/error.html", {
                    "message": "An entry with this title already exists."
                })

            util.save_entry(title, content)
            return redirect(f"/wiki/{title}")
    else:
        form = NewEntryForm()

    return render(request, "encyclopedia/create.html", {
        "form": form
    })

def edit(request, title):
    if request.method == "POST":
        content = request.POST.get("content")
        util.save_entry(title, content)
        return redirect("entry", title=title)

    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "The requested page was not found."
        })

    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content
    })


def random_page(request):
    entries = util.list_entries()
    if entries:
        title = random.choice(entries)
        return redirect("entry", title=title)
    else:
        return render(request, "encyclopedia/error.html", {
            "message": "No entries available."
        })
