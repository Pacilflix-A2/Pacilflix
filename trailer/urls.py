from django.urls import path
from .views import *

urlpatterns = [
    # ...
    path('', trailer, name='trailer'),
]