from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from . import util

import random
import markdown2

ERROR_NOT_FOUND = "Couldn't find any page called"
ERROR_PAGE_DUPLICATE = "This page already exists, failed to create"

class SearchForm(forms.Form):
    key = forms.CharField(label="Search")

class AddForm(forms.Form):
    title = forms.CharField(label="Page title")
    content = forms.CharField(widget=forms.Textarea)    

class EditForm(forms.Form):
    title = forms.CharField(label="Page title")
    content = forms.CharField(widget=forms.Textarea)

def index(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            key = form.cleaned_data["key"]
            if key in util.list_entries():
                return render_entry(request, key)
            else:
                entries = util.list_entries()
                matches = []
                for entry in entries:
                    if key in entry:
                        matches.append(entry)
                if not matches:
                    return error(request, key, ERROR_NOT_FOUND)
                else:
                    return search_page(request, matches, key)
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(), "form": SearchForm()
    })

def render_entry(request, title):
    if util.get_entry(title) != None:
        text = markdown2.markdown(util.get_entry(title))    
        return render(request, "encyclopedia/entry.html", {
        "title": title, "text": text, "form": SearchForm()
        })
    else:
        return error(request, title, ERROR_NOT_FOUND)

def error(request, title, message):
    return render(request, "encyclopedia/error.html", {
        "message": message, "title": title, "form": SearchForm()
    })

def search_page(request, matches, key):
    return render (request, "encyclopedia/search_page.html", {
        "key": key,"matches": matches, "form": SearchForm(), "entries": util.list_entries()
    })

def add_page(request):
    if request.method == "POST":
        add_form = AddForm(request.POST)
        if add_form.is_valid():
            title = add_form.cleaned_data["title"]            
            if title in util.list_entries():
                return error(request, title, ERROR_PAGE_DUPLICATE)
            else:
                content = add_form.cleaned_data["content"]
                util.save_entry(title, content)
                #return render_entry(request, title)
                return redirect(f"wiki/{title}")
                
    return render(request, "encyclopedia/add_page.html", {
        "add_form": AddForm()
    })

def edit_page(request, title):
    return render(request, "encyclopedia/edit_page.html", {
        "title": title, "content": util.get_entry(title)
    })

def save_changes(request):
    if request.method == "POST":
        edit_form = EditForm(request.POST)
        if edit_form.is_valid():
            title = edit_form.cleaned_data["title"]
            content = edit_form.cleaned_data["content"]
            util.save_entry(title, content)
            return redirect(f"wiki/{title}")
    return error(request, request.POST.get('title'), ERROR_PAGE_DUPLICATE)

def random_page(request):
    entries = util.list_entries()
    entry = entries[random.randint(0, len(entries)-1)]
    return redirect(f"wiki/{entry}")