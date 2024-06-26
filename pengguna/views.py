from django.shortcuts import render
from django.contrib import messages 
from django.http import HttpResponseRedirect
from django.urls import reverse
from general.query import *
from general.auth import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import format_html

@csrf_exempt
def register(request):
    if request.COOKIES.get('is_authenticated', '') == "True":
        return HttpResponseRedirect(reverse("tayangan_list"))

    context = {}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password1")
        asal_negara = request.POST.get("negara")
        
        try:
            add_query("INSERT INTO pengguna (username, password, asal_negara) VALUES (%s, %s, %s);", (username, password, asal_negara))
            messages.success(request, 'Your account has been successfully created!')
            response = HttpResponseRedirect(reverse("pengguna:login"))
            return response
        except Exception as e:
            error_message = str(e)
            messages.error(request, error_message.split("CONTEXT")[0].strip() )

    return render(request, 'register.html', context)
  
@csrf_exempt
def login_user(request):
    if request.COOKIES.get('is_authenticated', '') == "True":
        return HttpResponseRedirect(reverse("tayangan_list"))

    context = {}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        result = query_select('SELECT username, asal_negara FROM pengguna WHERE username = %s AND password = %s', (username, password))
        
        if len(result) != 0:
            username = result[0][0]
            negara = result[0][1]
            response = HttpResponseRedirect(reverse("tayangan_list"))

            response.set_cookie('username', username)
            response.set_cookie('negara', negara)
            response.set_cookie('is_authenticated', "True")
            messages.success(request, format_html("Login Success. Welcome, <strong>{}</strong>!", username))
            return response
        else:
            messages.error(request, "Sorry, incorrect username or password. Please try again.")

    return render(request, 'login.html', context)

def logout_user(request):
    response = HttpResponseRedirect(reverse('main:show_main'))

    response.delete_cookie('username')
    response.delete_cookie('negara')
    response.delete_cookie('is_authenticated')
    
    return response
