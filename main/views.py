from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render

# Create your views here.
def show_main(request):
    return render(request, "main.html")

