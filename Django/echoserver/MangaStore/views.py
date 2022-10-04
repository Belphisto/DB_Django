from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.urls import is_valid_path
from .forms import MangaForm
from .models import Manga

# Create your views here.

# получение данных из бд
def home(request):
    manga = Manga.objects.all()
    return render(request, "home.html", {"manga" : manga})

def add(request):
    userForm = MangaForm()
    return render(request, "addManga.html", {"form":userForm})


# сохранение данных в бд
def create(request):
    if request.method == "GET":
        return render(request, "addManga.html")
    manga = Manga()
    manga.name = request.POST.get("name")
    manga.author = request.POST.get("author")
    manga.price = request.POST.get("price")
    manga.save()
    return HttpResponseRedirect("/")

# изменение данных в бд
def edit(request, id):
    try:
        manga = Manga.objects.get(id=id)
        if request.method == "POST":
            manga.name = request.POST.get("name")
            manga.author = request.POST.get("author")
            manga.price = request.POST.get("price")
            manga.save()
            return HttpResponseRedirect("/")
        else:
            return render(request, "editManga.html", {"manga": manga})
    except Manga.DoesNotExist:
        return HttpResponseNotFound("<h2>Manga not found</h2>")

# удаление данных из бд
def delete(request, id):
    try:
        manga = Manga.objects.get(id=id)
        manga.delete()
        return HttpResponseRedirect("/")
    except Manga.DoesNotExist:
        return HttpResponseNotFound("<h2>Manga not found</h2>")