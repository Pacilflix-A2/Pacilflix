from django.urls import path
from daftar.views import *

app_name = 'daftar'

urlpatterns = [
    path('daftar_favorit', daftar_favorit, name='daftar_favorit'),
    path('daftar_unduhan', daftar_unduhan, name='daftar_unduhan'),
]