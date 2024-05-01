import datetime
from django.shortcuts import render, redirect


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