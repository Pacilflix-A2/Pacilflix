from django.urls import path
from . import views
urlpatterns = [
    path('', views.tayangan_list, name='tayangan_list'),
    path('hasil_pencarian/', views.hasil_pencarian, name='hasil_pencarian'),
    path('film/<str:film_id>/', views.detail_tayangan_film, name='detail_tayangan_film'),
    path('series/<str:series_id>/', views.detail_tayangan_series, name='detail_tayangan_series'),
    path('episode/<str:episode_id>/', views.detail_tayangan_episode, name='detail_tayangan_episode'),
    path('film/<str:film_id>/watch/', views.record_film_watch, name='record_film_watch'),
    path('series/<str:series_id>/watch/', views.record_series_watch, name='record_series_watch'),
]