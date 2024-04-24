from django.urls import path
from daftar.views import daftar_favorit, daftar_unduhan

urlpatterns = [
    path('favorit', daftar_favorit, name='daftar_favorit'),
    path('unduhan', daftar_unduhan, name='daftar_unduhan'),
]