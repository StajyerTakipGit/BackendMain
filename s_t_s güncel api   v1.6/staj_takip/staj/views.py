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
from .models import HesapTalep, Kullanici
from .serializers import HesapTalepSerializer
from django.contrib.auth.hashers import make_password
import random
import string



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
        

# 2️ Staj başvurusunu güncelle (onayla/puanla)
class KurumStajUpdateAPIView(generics.UpdateAPIView):
    serializer_class = StajSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Staj.objects.all()

    def perform_update(self, serializer):
        staj = serializer.save()

        # Durumu güncelle: onaylandıysa aktif, reddedildiyse reddedildi
        if staj.kurum_onaylandi:
            staj.durum = "Aktif"
        else:
            staj.durum = "Reddedildi"
        staj.save()

        # Eğer kurum onay verdiyse, öğrenciye e-posta gönder
        if staj.kurum_onaylandi:
            send_mail(
                subject='Staj Başvurunuz Onaylandı ✅',
                message=f"{staj.kurum_adi} tarafından onaylandı.",
                from_email=None,
                recipient_list=[staj.ogrenci.email],
                fail_silently=True
            )




# otomatik kullanıcı oluşturma ve şifreleme mail gönderimi

# Başvuru yapan kullanıcılar için
class HesapTalepCreateAPIView(generics.CreateAPIView):
    serializer_class = HesapTalepSerializer
    permission_classes = [permissions.AllowAny]

# Admin'in tüm başvuruları listeleyebilmesi için
class HesapTalepListAPIView(generics.ListAPIView):
    serializer_class = HesapTalepSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = HesapTalep.objects.filter(onaylandi=False)

# Admin onay verip otomatik kullanıcı oluşturma işlemi
class HesapTalepOnayAPIView(generics.UpdateAPIView):
    serializer_class = HesapTalepSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = HesapTalep.objects.all()

    def update(self, request, *args, **kwargs):
        talep = self.get_object()
        if talep.onaylandi:
            return Response({'detail': 'Zaten onaylanmış.'}, status=400)

        # Kullanıcıyı oluştur
        Kullanici.objects.create_user(
            email=talep.email,
            password="12345678",  # veya random üretilip e-postalanabilir
            isim=talep.isim,
            rol=talep.rol,
            is_staff=(talep.rol == 'ADMIN')
        )

        # Talep onaylandı olarak işaretle
        talep.onaylandi = True
        talep.save()

        # Bilgilendirme maili gönder
        send_mail(
            subject="Hesabınız Onaylandı",
            message="Sisteme giriş yapabilirsiniz. Şifreniz: 12345678",
            recipient_list=[talep.email],
            from_email=None,
            fail_silently=True,
        )

        return Response({'detail': 'Kullanıcı oluşturuldu ve e-posta gönderildi.'}, status=status.HTTP_200_OK)
    
    # random şifre ataması
    def generate_password(length=8):
         return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

        # sonra view içinde:
    sifre = generate_password() 