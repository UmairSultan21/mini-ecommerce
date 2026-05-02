from django.shortcuts import render

# Create your views here.

from django.shortcuts import render

def login_view(request):

    return render(request, "users/login.html")

def register(request):

    return render(request, "users/register.html")

def forgot_password(request):

    return render(request, "users/forgot_password.html")

def profile(request):

    return render(request, "users/profile.html")

def edit_profile(request):

    return render(request, "users/edit_profile.html")
