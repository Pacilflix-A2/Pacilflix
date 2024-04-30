from django.urls import path
from . import views

urlpatterns = [
    path('', views.tayangan_list, name='tayangan_list'),
    path('hasil_pencarian/', views.hasil_pencarian, name='hasil_pencarian'),
]