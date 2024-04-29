from django.shortcuts import render

# Create your views here.
def trailer(request):
    return render(request, 'trailer/trailer.html')