from django.urls import path
from .views import trailer

urlpatterns = [
    # ...
    path('', trailer, name='trailer'),
    # ...
]