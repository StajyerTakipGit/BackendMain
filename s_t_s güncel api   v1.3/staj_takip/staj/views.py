from django.shortcuts import render

from rest_framework import generics, permissions
from .models import Staj, StajDefteri
from .serializers import StajSerializer, StajDefteriSerializer
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView




class StajDefteriUpdateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, staj_id):
        gun_no = request.data.get('gun_no')
        yeni_icerik = request.data.get('icerik')

        if not gun_no or not yeni_icerik:
            return Response({'hata': 'gun_no ve icerik alanları zorunludur.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            defter_girdisi = StajDefteri.objects.get(
                staj__id=staj_id,
                staj__ogrenci=request.user,
                gun_no=gun_no
            )
        except StajDefteri.DoesNotExist:
            return Response({'hata': 'Belirtilen güne ait kayıt bulunamadı.'}, status=status.HTTP_404_NOT_FOUND)

        defter_girdisi.icerik = yeni_icerik
        defter_girdisi.save()

        return Response({'basari': 'İçerik güncellendi.'}, status=status.HTTP_200_OK)

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