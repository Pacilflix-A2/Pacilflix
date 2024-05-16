from django.urls import path
from pengguna.views import *

app_name = 'pengguna'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
]