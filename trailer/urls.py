from django.urls import path
from .views import *

urlpatterns = [
    # ...
    path('', trailer, name='trailer'),
    path('test/', trailer_test, name='trailer_test'),
]