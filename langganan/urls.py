from django.urls import path
from langganan.views import kelola, beli

urlpatterns = [
    path('kelola', kelola, name='kelola'),
    path('beli', beli, name='beli'),
]