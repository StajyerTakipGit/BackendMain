from django.shortcuts import render

from rest_framework import generics, permissions
from staj.models import Staj
from staj.serializers import StajSerializer
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend

class AdminStajListAPIView(generics.ListAPIView):
    serializer_class = StajSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Staj.objects.all()
    

class AdminStajOnayAPIView(generics.UpdateAPIView):
    serializer_class = StajSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Staj.objects.all()

    def perform_update(self, serializer):
        staj = serializer.save()

        # Durum kontrolü: Kurum onayladıysa ve şimdi admin de onaylıyorsa "Aktif" yap
        if staj.kurum_onaylandi and staj.admin_onaylandi:
            staj.durum = "Aktif"

            # Öğrenciye bilgilendirme e-postası gönder
            send_mail(
                subject='🎓 Staj Başvurunuz Onaylandı!',
                message=f"Sayın {staj.ogrenci.isim}, {staj.kurum_adi} tarafından onaylanan staj başvurunuz artık üniversite tarafından da onaylandı. Staj süreciniz başlamıştır.",
                from_email=None,
                recipient_list=[staj.ogrenci.email],
                fail_silently=True
            )

        # Eğer kurum onayı varsa ama admin onayı verilmediyse, "Kurum Onayladı" olarak kalır
        elif staj.kurum_onaylandi and not staj.admin_onaylandi:
            staj.durum = "Kurum Onayladı"

        # Reddedilmişse veya iptal edilmişse
        else:
            staj.durum = "Reddedildi"

        staj.save()


class AdminFilteredStajListAPIView(generics.ListAPIView):
    serializer_class = StajSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['durum', 'konu', 'baslangic_tarihi', 'ogrenci__isim']

    def get_queryset(self):
        return Staj.objects.filter(kurum_onaylandi=True)