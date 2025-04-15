from django.urls import path
from .views import AdminStajListAPIView, AdminStajOnayAPIView

urlpatterns = [
    path('admin/stajlar/', AdminStajListAPIView.as_view(), name='admin-staj-listesi'),
    path('admin/stajlar/<int:pk>/', AdminStajOnayAPIView.as_view(), name='admin-staj-onay'),
]