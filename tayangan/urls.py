from django.urls import path
from . import views
urlpatterns = [
    path('', views.tayangan_list, name='tayangan_list'),
    path('film/<str:film_id>/', views.detail_tayangan_film, name='detail_tayangan_film'),
    path('series/<str:series_id>/', views.detail_tayangan_series, name='detail_tayangan_series'),
    path('episode/<str:episode_id>/', views.detail_tayangan_episode, name='detail_tayangan_episode'),
    path('film/<str:film_id>/watch/', views.record_film_watch, name='record_film_watch'),
    path('series/<str:series_id>/watch/', views.record_series_watch, name='record_series_watch'),
    path('submit-review/<str:tayangan_id>/', views.submit_review, name='submit_review'),
    path('unduh-tayangan/<str:tayangan_id>/', views.unduh_tayangan, name='unduh_tayangan'),
]