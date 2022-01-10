from django.shortcuts import redirect, render
from django import forms

from random import choice
from markdown2 import Markdown

from . import util


class NewPageForm(forms.Form):
    title_form = forms.CharField(
        max_length=255,
        min_length=3,
        label="Title"
    )
    content_form = forms.CharField(
        widget=forms.Textarea(),
        min_length=50,
        required=True,
        label="Content"
    )

    class Meta:
        fields = ["title_form", "content_form"]

class EditPageForm(forms.Form):
    title_form = forms.CharField(
        widget=forms.TextInput(attrs={"readonly": "readonly"}),
        label="Title"
    )
    content_form = forms.CharField(
        widget=forms.Textarea(),
        min_length=50,
        required=True,
        label="Content"
    )

    class Meta:
        fields = ["title_form", "content_form"]


def convert_md_to_html(content):
    markdowner = Markdown()
    return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def get_page(request, title):
    return render(request, "encyclopedia/page.html", {
        "title": title.upper(),
        "page": convert_md_to_html(util.get_entry(title))
    })

def find_page(request):
    search = request.GET.get('q')
    entries = util.list_entries()
    if search in [entry.lower() for entry in entries]:
        return get_page(request, search)
    else:
        context = {
            "entries": [
                entry for entry in entries if search.lower() in entry.lower()
            ]
        }
        return render(request, "encyclopedia/search.html", context)

def create_page(request):
    save_error = False
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title_form"]
            content = form.cleaned_data["content_form"]
            if not util.get_entry(title):
                util.save_entry(title, content)
                return redirect(f"/wiki/{title}")
            else:
                save_error = f"Page '{title}' already exists!"
    else:
        form = NewPageForm()
    context = {"new_page_form": form, "save_error": save_error}
    return render(request, "encyclopedia/create_page.html", context)

def edit_page(request, title):
    content = util.get_entry(title)
    if request.method == "POST":
        form = EditPageForm(data=request.POST)
        if form.is_valid():
            title = form.cleaned_data["title_form"]
            content = form.cleaned_data["content_form"]
            util.save_entry(title, content)
            return redirect("page", f"{title}")
    else:
        form = EditPageForm(initial={"title_form": title,"content_form": content})
    context = {"edit_page_form": form, "title": title}
    return render(request, "encyclopedia/edit_page.html", context)

def get_random_page(request):
    random_entry = choice(util.list_entries())
    return get_page(request, random_entry)