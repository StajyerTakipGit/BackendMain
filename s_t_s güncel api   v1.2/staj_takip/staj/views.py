from django.shortcuts import render

from rest_framework import generics, permissions
from .models import Staj, StajDefteri
from .serializers import StajSerializer, StajDefteriSerializer
from django.core.mail import send_mail
from django.conf import settings


class StajListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = StajSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Staj.objects.filter(ogrenci=self.request.user)

    def perform_create(self, serializer):
        serializer.save(ogrenci=self.request.user)

class StajDetayAPIView(generics.RetrieveAPIView):
    serializer_class = StajSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Staj.objects.all()

class StajDefteriListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = StajDefteriSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        staj_id = self.kwargs['staj_id']
        return StajDefteri.objects.filter(staj__id=staj_id, staj__ogrenci=self.request.user)

    def perform_create(self, serializer):
        staj_id = self.kwargs['staj_id']
        staj = Staj.objects.get(id=staj_id, ogrenci=self.request.user)
        serializer.save(staj=staj)



# Kurum tarafı: stajyer listesi ve onay/puanlama
class KurumStajListAPIView(generics.ListAPIView):
    serializer_class = StajSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Staj.objects.filter(kurum_adi__icontains=self.request.user.email)  # örnek filtre mantığı

class KurumStajDetayUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = StajSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Staj.objects.all()

    def perform_update(self, serializer):
        staj = serializer.save()
        
        if staj.kurum_onaylandi:
            # HTML içerikli mail
            html_message = f"""
            <h2>Staj Başvuru Onayı</h2>
            <p>Merhaba <strong>{staj.ogrenci.isim}</strong>,</p>
            <p>{staj.kurum_adi} tarafından yapmış olduğunuz staj başvurusu onaylandı.</p>
            <p>Lütfen sistem üzerinden süreci takip ediniz.</p>
            <hr>
            <p><em>Staj Takip Sistemi</em></p>
            """
            
            send_mail(
                subject='Staj Başvurunuz Onaylandı ✅',
                message='',  # Boş bırakılıyor çünkü html_message kullanıyoruz
                from_email=None,  # DEFAULT_FROM_EMAIL otomatik kullanılır
                recipient_list=[staj.ogrenci.email],
                fail_silently=False,
                html_message=html_message  # HTML formatında mail
            )