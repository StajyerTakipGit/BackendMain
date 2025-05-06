from rest_framework import serializers
from .models import Staj, StajDefteri

class StajSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staj
        fields = '__all__'
        read_only_fields = ['ogrenci']

class StajDefteriSerializer(serializers.ModelSerializer):
    class Meta:
        model = StajDefteri
        fields = ['gun_no', 'icerik']
