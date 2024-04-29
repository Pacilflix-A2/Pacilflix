from django.urls import path
from daftar.views import daftar_favorit, daftar_unduhan

urlpatterns = [
    path('daftar_favorit', daftar_favorit, name='daftar_favorit'),
    path('daftar_unduhan', daftar_unduhan, name='daftar_unduhan'),
]