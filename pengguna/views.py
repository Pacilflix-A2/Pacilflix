import datetime
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from query.query import *
from query.auth import *


def register(request):
    # if request.user.is_authenticated:
    #     return HttpResponseRedirect(reverse("main:show_main")) # Ubah ke halaman daftar tayangan

    # form = UserRegisterForm()

    # if request.method == "POST":
    #     form = UserRegisterForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request, 'Your account has been successfully created!')
    #         return redirect('pengguna:login')
    # context = {'form':form}
    return render(request, 'register.html')

def login_user(request):
    # if request.user.is_authenticated:
    #     return HttpResponseRedirect(reverse("main:show_main"))  # Ubah ke halaman daftar tayangan
        
    # if request.method == 'POST':
    #     username = request.POST.get('username')
    #     password = request.POST.get('password')

    #     user = authenticate(request, username=username, password=password)

    #     if user is not None:
    #         login(request, user)
    #         response = HttpResponseRedirect(reverse("main:show_main")) 
    #         response.set_cookie('last_login', str(datetime.datetime.now()))
    #         return response
    #     else:
    #         messages.info(request, 'Sorry, incorrect username or password. Please try again.')
    # context = {}
    return render(request, 'login.html')

def logout_user(request):
    return redirect('main:show_main')

#Hafiz make
def login(request):
    context = {"error": ""}
    if request.method == "POST":
        # GET DATA
        nama = request.POST.get("username")
        password = request.POST.get("password")
        result = query_sql(f"SELECT username, asal_negara FROM pengguna WHERE username='{nama}' AND password='{password}';")
        print(result)
        
        if len(result) != 0:
            username = result[0][0]
            negara = result[0][1]
            response = HttpResponseRedirect(reverse("tayangan_list"))
            
            # SET COOKIES
            response.set_cookie('username', username)
            response.set_cookie('negara', negara)
            response.set_cookie('is_authenticated', "True")
            
            # REDIRECT
            return response
        else:
            context = {"is_error": True}

    return render(request, 'login.html', context)

def logout(request):
    # DELETE COOKIES
    response = HttpResponseRedirect(reverse('main:show_main'))
    response.delete_cookie('username')
    response.delete_cookie('negara')
    response.delete_cookie('is_authenticated')

    return response