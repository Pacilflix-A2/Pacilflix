from django.shortcuts import render
from django.contrib import messages 
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse

from general.query import *

def register(request):
    if request.COOKIES.get('is_authenticated', '') == "True":
        return HttpResponseRedirect(reverse("main:show_main")) # Ubah ke halaman daftar tayangan

    context = {"error": ""}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password1")
        asal_negara = request.POST.get("negara")
        
        try:
            add_query(f"INSERT INTO pengguna (username, password, asal_negara) VALUES ('{username}', '{password}', '{asal_negara}');")
            messages.success(request, 'Your account has been successfully created!')
            response = HttpResponseRedirect(reverse("pengguna:login"))
            return response
        except IntegrityError:
            context["error"] = f"Username {username} already exists."

    return render(request, 'register.html', context)

def login_user(request):
    if request.COOKIES.get('is_authenticated', '') == "True":
        return HttpResponseRedirect(reverse("main:show_main")) # Ubah ke halaman daftar tayangan

    context = {"error": ""}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        result = query_select(f"SELECT username, asal_negara FROM pengguna WHERE username='{username}' AND password='{password}';")
        
        if len(result) != 0:
            username = result[0][0]
            negara = result[0][1]
            response = HttpResponseRedirect(reverse("main:show_main")) # Ubah ke halaman daftar tayangan

            response.set_cookie('username', username)
            response.set_cookie('negara', negara)
            response.set_cookie('is_authenticated', "True")
            
            return response
        else:
            context["error"] = "Sorry, incorrect username or password. Please try again."

    return render(request, 'login.html', context)

def logout_user(request):
    response = HttpResponseRedirect(reverse('main:show_main')) # Ubah ke halaman trailer tayangan

    response.delete_cookie('username')
    response.delete_cookie('negara')
    response.delete_cookie('is_authenticated')
    
    return response