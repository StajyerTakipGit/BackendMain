from rest_framework import serializers
from .models import Kullanici
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class KullaniciSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kullanici
        fields = ['id', 'email', 'isim', 'soyisim', 'rol']

class TokenAlSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['rol'] = self.user.rol
        data['isim'] = self.user.isim
        data['soyisim'] = self.user.soyisim
        return data