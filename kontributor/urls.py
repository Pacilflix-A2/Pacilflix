from django.urls import path
from kontributor.views import kontributor

urlpatterns = [
    path('', kontributor, name='kontributor'),
]