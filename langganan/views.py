from django.shortcuts import render

# Create your views here.
def kelola(request):
    return render(request, "kelola.html")

def beli(request):
    return render(request, "beli.html")