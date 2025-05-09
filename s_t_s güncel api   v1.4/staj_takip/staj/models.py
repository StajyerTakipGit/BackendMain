from django.db import models
from kullanici.models import Kullanici

class Staj(models.Model):
    ogrenci = models.ForeignKey(Kullanici, on_delete=models.CASCADE, related_name='stajlar')
    
    kurum_adi = models.CharField(max_length=100)
    baslangic_tarihi = models.DateField()
    bitis_tarihi = models.DateField()
    konu = models.TextField()

    # Kurum onaylama bilgileri
    kurum_onaylandi = models.BooleanField(default=False)
    kurum_puani = models.IntegerField(null=True, blank=True)
    kurum_aciklama = models.TextField(null=True, blank=True)


    

    def __str__(self):
        return f"{self.ogrenci.isim} - {self.kurum_adi}"

class StajDefteri(models.Model):
    staj = models.ForeignKey(Staj, on_delete=models.CASCADE, related_name='defter_girdileri')
    gun_no = models.DateField()
    icerik = models.TextField()
    tarih = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Gün {self.gun_no} - {self.staj}"