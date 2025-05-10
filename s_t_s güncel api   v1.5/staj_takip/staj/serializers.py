from rest_framework import serializers
from .models import Staj, StajDefteri
from kullanici.models import Kullanici
from .models import HesapTalep

class StajSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staj
        fields = '__all__'
        read_only_fields = ['ogrenci']

class StajDefteriSerializer(serializers.ModelSerializer):
    class Meta:
        model = StajDefteri
        fields = ['gun_no', 'icerik']


class KullaniciMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kullanici
        fields = ['isim', 'soyisim', 'email']


class StajSerializer(serializers.ModelSerializer):
    ogrenci = KullaniciMiniSerializer(read_only=True)

    class Meta:
        model = Staj
        fields = '__all__'


class HesapTalepSerializer(serializers.ModelSerializer):
    class Meta:
        model = HesapTalep
        fields = '__all__'
        read_only_fields = ['onaylandi', 'tarih']

