from django.urls import path
from daftar.views import *

app_name = 'daftar'

urlpatterns = [
    path('daftar_favorit', daftar_favorit, name='daftar_favorit'),
    path('daftar_unduhan', daftar_unduhan, name='daftar_unduhan'),
    path('delete', delete_downloaded_item, name='delete_unduhan'),
    path('delete_favorit', delete_favorit_item, name='delete_favorit'),
]