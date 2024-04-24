from django.urls import path
from daftar.views import daftar_favorit

urlpatterns = [
    path('favorit', daftar_favorit, name='daftar_favorit'),
]