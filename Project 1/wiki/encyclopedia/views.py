from django.shortcuts import render
import markdown2
from . import util
import random



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def convert(title):
    content = util.get_entry(title)
    if content == None:
        return None
    else:
        return markdown2.markdown(content)


def entry(request, title):
    html_content = convert(title)
    if html_content == None:
        return render(request, "encyclopedia/error.html", {
            "message": "Entry not found in the system"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })
        
        
def search(request):
    if request.method == "POST":
        entry_search = request.POST['q']
        html_content = convert(entry_search)
        if html_content is not None:
            return render(request, "encyclopedia/entry.html", {
                "title": entry_search,
                "content": html_content
            })
        else:
            allEntries = util.list_entries()
            reccomendation = []
            for entry in allEntries:
                if entry_search.lower() in entry.lower():
                    reccomendation.append(entry)
                    
            if len(reccomendation) == 0:
                return render(request, "encyclopedia/search.html", {
                    "message": f"{entry_search} not found in the system",
                })
                
            return render(request, "encyclopedia/search.html", {
                "reccomendation": reccomendation
            })


def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new_page.html")
    else:
        title = request.POST["title"]
        content = request.POST["content"]
        titleExist = util.get_entry(title)
        if titleExist is not None:
            return render(request, "encyclopedia/error.html", {
                "message": "Entry page already exist"
            })
        else:
            util.save_entry(title, content)
            html_content = convert(title)
            return render(request, "encyclopdia/entry.html", {
                "title": title,
                "content": html_content
            })
            
            
def edit(request):
    if request.method == "POST":
        title = request.POST["entry-title"]
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            'content': content
        })
        
        
def save_edit(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        html_content = convert(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })


def random_page(request):
    if request.method == "GET":
        allEntries = util.list_entries()
        title = random.choice(allEntries)
        html_content = convert(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })