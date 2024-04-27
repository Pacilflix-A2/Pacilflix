from django.shortcuts import render, redirect

from django.contrib import messages 
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.forms import UserCreationForm

def register(request):
    return render(request, 'register.html')

def login_user(request):
    return render(request, 'login.html')

def logout_user(request):
    return redirect('pengguna:login')