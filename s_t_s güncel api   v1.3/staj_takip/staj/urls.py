from django.urls import path
from .views import (
    StajListCreateAPIView, StajDetayAPIView, StajDefteriListCreateAPIView,
    KurumStajListAPIView, KurumStajDetayUpdateAPIView
)
from .views import StajDefteriUpdateAPIView

urlpatterns = [
    # Öğrenci
    path('ogrenci/stajlar/', StajListCreateAPIView.as_view(), name='staj-listesi'),
    path('ogrenci/stajlar/<int:pk>/', StajDetayAPIView.as_view(), name='staj-detay'),
    path('ogrenci/stajlar/<int:staj_id>/defter/', StajDefteriListCreateAPIView.as_view(), name='staj-defter'),
    path('ogrenci/stajlar/<int:staj_id>/defter/guncelle/', StajDefteriUpdateAPIView.as_view(), name='defter-guncelle'),



    # Kurum
    path('kurum/stajyerler/', KurumStajListAPIView.as_view(), name='kurum-stajyerler'),
    path('kurum/stajyerler/<int:pk>/', KurumStajDetayUpdateAPIView.as_view(), name='kurum-onay'),
]