from django.db import models
from kullanici.models import Kullanici

class Staj(models.Model):

    DURUM_SECENEKLERI = [
        ('Beklemede', 'Beklemede'),
        ('Aktif', 'Aktif'),
        ('Tamamlandı', 'Tamamlandı'),
        ('Reddedildi', 'Reddedildi'),
    ]
    ogrenci = models.ForeignKey(Kullanici, on_delete=models.CASCADE, related_name='stajlar')
    
    kurum_adi = models.CharField(max_length=100)
    baslangic_tarihi = models.DateField()
    bitis_tarihi = models.DateField()
    konu = models.TextField()

    # Kurum onaylama bilgileri
    kurum_onaylandi = models.BooleanField(default=False)
    kurum_puani = models.IntegerField(null=True, blank=True)
    kurum_aciklama = models.TextField(null=True, blank=True)
    admin_onaylandi = models.BooleanField(default=False)
    durum = models.CharField(
        max_length=20,
        choices=DURUM_SECENEKLERI,
        default='Beklemede'
    )


    

    def __str__(self):
        return f"{self.ogrenci.isim} - {self.kurum_adi}"

class StajDefteri(models.Model):
    staj = models.ForeignKey(Staj, on_delete=models.CASCADE, related_name='defter_girdileri')
    gun_no = models.DateField()
    icerik = models.TextField()
    tarih = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Gün {self.gun_no} - {self.staj}"
    





    # staj/models.py 
    # hesap talep modelim

class HesapTalep(models.Model):
    ROL_SECENEKLERI = [
        ('OGRENCI', 'Öğrenci'),
        ('KURUM', 'Kurum'),
    ]
    email = models.EmailField(unique=True)
    isim = models.CharField(max_length=50)
    rol = models.CharField(max_length=10, choices=ROL_SECENEKLERI)
    onaylandi = models.BooleanField(default=False)
    tarih = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} ({self.rol})"
