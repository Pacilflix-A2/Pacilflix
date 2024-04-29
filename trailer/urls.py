from django.urls import path
from .views import trailer

app_name = 'trailer'

urlpatterns = [
    # ...
    path('trailer/', trailer, name='trailer'),
    # ...
]