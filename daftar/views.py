from django.shortcuts import render

# Create your views here.
def daftar_favorit(request):
    return render(request, "daftar_favorit.html")

def daftar_unduhan(request):
    return render(request, "daftar_unduhan.html")