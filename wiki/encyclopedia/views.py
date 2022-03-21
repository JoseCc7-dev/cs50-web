from django.shortcuts import render

from . import util
import random
from markdown2 import Markdown
from flask import redirect

markdown = Markdown()
def index(request):
    if request.method == 'POST':
        form = request.POST
        title = form.get('title')
        entries = util.list_entries()
        print(form)
        for i in entries:
            if title.upper() in i.upper():
                message = 'Entry already exists' 
                return render(request, "encyclopedia/error.html", {
                    "message": message
                })
        else:    
            f = open("entries/{}.md".format(title.capitalize()), "w")
            f.write(form.get('content'))
            f.close()
            return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })

def newPage(request):
    return render(request, "encyclopedia/newPage.html")

def randomPage(request):
    title = random.choice(util.list_entries())
    entry = markdown.convert(util.get_entry(title))
    return render(request, "encyclopedia/loadPage.html", {
            "entry": entry, "title": title
    })

def loadPage(request, entry):
    title = entry
    entry = markdown.convert(util.get_entry(title))
    if request.method == "POST":
        form = request.POST
        f = open("entries/{}.md".format(title.capitalize()), "w")
        f.write(form.get('content'))
        f.close()
        return render(request, "encyclopedia/loadPage.html", {
            "entry": entry, "title": title
        })
    if not entry:
        message = 'No page found for requested entry' 
        return render(request, "encyclopedia/error.html", {
            "message": message
        })
    else:
        # entry = entry.split('\n')
        return render(request, "encyclopedia/loadPage.html", {
            "entry": entry, "title": title
        })

def search(request):
    form = request.GET.get('q', '0')
    query = form
    
    if query in util.list_entries():
        loadPage(request, query)
    else: 
        entries = util.list_entries()
        options = []
        for i in entries:
            if query.upper() in i.upper():
                options.append(i) 
        return render(request, "encyclopedia/search.html", {
            "entries": options
    })

def editPage(request):
    form = request.GET
    title = form.get('title')
    entry = util.get_entry(title).split('\n')
    content = []
    for i in range(0, len(entry)):
        if i < len(entry)-1:
            word = entry[i]
            temp = word[:-1]
            content.append(temp)
        else:
            content.append(entry[i])
    return render(request, "encyclopedia/loadPage.html",{
        "editcontent": content, "title":title
    })