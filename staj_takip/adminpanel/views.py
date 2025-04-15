from django.shortcuts import render

from rest_framework import generics, permissions
from staj.models import Staj
from staj.serializers import StajSerializer
from django.core.mail import send_mail

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
        if staj.kurum_onaylandi:
            send_mail(
                subject='Staj Onayı Bekliyor',
                message=f"{staj.ogrenci.isim} {staj.ogrenci.soyisim} adlı öğrencinin stajı kurum tarafından onaylandı. Lütfen kontrol ediniz.",
                from_email=None,
                recipient_list=['admin@universite.com'],
                fail_silently=True,
            )
