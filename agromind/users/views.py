from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages

def user_login(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
        if user:
            login(request, user)
            return redirect("dashboard")
        messages.error(request, "Invalid username or password.")
    return render(request, "users/login.html")

def user_signup(request):
    if request.method == "POST":
        u = request.POST["username"]
        if User.objects.filter(username=u).exists():
            messages.error(request, "Username already taken.")
            return render(request, "users/signup.html")
        user = User.objects.create_user(username=u,
            email=request.POST.get("email",""), password=request.POST["password"])
        login(request, user)
        return redirect("dashboard")
    return render(request, "users/signup.html")

def user_logout(request):
    logout(request)
    return redirect("login")
