from django.shortcuts import render

from rest_framework import generics, permissions
from .models import Staj, StajDefteri
from .serializers import StajSerializer, StajDefteriSerializer
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied




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
        user = self.request.user
        if user.rol != "KURUM":
            raise PermissionDenied("Sadece kurum kullanıcıları erişebilir.")
        return Staj.objects.filter(kurum_adi__icontains=user.email)  # örnek eşleşme
        

# 2️⃣ Staj başvurusunu güncelle (onayla/puanla)
class KurumStajUpdateAPIView(generics.UpdateAPIView):
    serializer_class = StajSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Staj.objects.all()

    def perform_update(self, serializer):
        staj = serializer.save()

        # Eğer kurum onay verdiyse, öğrenciye e-posta gönder
        if staj.kurum_onaylandi:
            send_mail(
                subject='Staj Başvurunuz Onaylandı ✅',
                message=f"{staj.kurum_adi} tarafından onaylandı.",
                from_email=None,
                recipient_list=[staj.ogrenci.email],
                fail_silently=True
            )