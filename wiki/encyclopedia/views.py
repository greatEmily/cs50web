from django.shortcuts import render, redirect

from . import util

import markdown2

#from django.http import HttpResponse

#def test_entry(request, title):
    #return HttpResponse(f"Title received: {title}")

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