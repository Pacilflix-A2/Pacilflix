from django.urls import path
from . import views

urlpatterns = [
    path('', views.tayangan_list, name='tayangan_list'),
    path('hasil_pencarian/', views.hasil_pencarian, name='hasil_pencarian'),
    path('film/', views.detail_tayangan_film, name='detail_tayangan_film'),
    path('series/', views.detail_tayangan_series, name='detail_tayangan_series'),
    path('episode/', views.detail_tayangan_episode, name='detail_tayangan_episode')
]