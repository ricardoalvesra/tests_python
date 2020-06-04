from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import RegisterForm

# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return render(request, "pizza/login.html", {"message": None})
    context = {
        "user": request.user
    }
    return render(request, "pizza/user.html", context)

def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "pizza/login.html", {"message": "Invalid credentials."})

def logout_view(request):
    logout(request)
    return render(request, "pizza/login.html", {"message": "Logged out."})

def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()

        return HttpResponseRedirect(reverse("index"))
    else:
        form = RegisterForm()

    return render(response, "pizza/register.html", {"form":form})