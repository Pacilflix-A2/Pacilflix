from django.urls import path
from langganan.views import kelola, display_beli, process_purchase

urlpatterns = [
    path('kelola', kelola, name='kelola'),
    path('beli/<str:nama_paket>/', display_beli, name='display_beli'),
    path('process-purchase/', process_purchase, name='process_purchase'),
    
]