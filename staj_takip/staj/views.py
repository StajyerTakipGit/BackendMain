from django.shortcuts import render

from rest_framework import generics, permissions
from .models import Staj, StajDefteri
from .serializers import StajSerializer, StajDefteriSerializer

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