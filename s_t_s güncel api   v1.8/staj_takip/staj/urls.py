from django.urls import path
from .views import (
    StajListCreateAPIView, StajDetayAPIView, StajDefteriListCreateAPIView,
    KurumStajListAPIView, KurumStajUpdateAPIView
)
from .views import StajDefteriUpdateAPIView

from .views import (
    HesapTalepCreateAPIView,
    HesapTalepListAPIView,
    HesapTalepOnayAPIView,
)

urlpatterns = [
    # Öğrenci
    path('ogrenci/stajlar/', StajListCreateAPIView.as_view(), name='staj-listesi'),
    path('ogrenci/stajlar/<int:pk>/', StajDetayAPIView.as_view(), name='staj-detay'),
    path('ogrenci/stajlar/<int:staj_id>/defter/', StajDefteriListCreateAPIView.as_view(), name='staj-defter'),
    path('ogrenci/stajlar/<int:staj_id>/defter/guncelle/', StajDefteriUpdateAPIView.as_view(), name='defter-guncelle'),



    # Kurum
    path('kurum/stajyerler/', KurumStajListAPIView.as_view(), name='kurum-stajyerler'),
    path('kurum/stajlar/<int:pk>/', KurumStajUpdateAPIView.as_view(), name='kurum-staj-update'),


    # hesap ekleme ve tanımlama 

    path('hesap-talep/', HesapTalepCreateAPIView.as_view(), name='talep-olustur'),
    path('hesap-talep-listesi/', HesapTalepListAPIView.as_view(), name='admin-talepler'),
    path('hesap-talep-onayla/<int:pk>/', HesapTalepOnayAPIView.as_view(), name='talep-onayla'),
]