from django.core.management.base import BaseCommand
from kullanici.models import Kullanici
from staj.models import Staj, StajDefteri
from django.utils import timezone
from datetime import timedelta, date

class Command(BaseCommand):
    help = 'Test verilerini yükler'

    def handle(self, *args, **kwargs):
        # Öğrenci oluştur
        ogrenci, _ = Kullanici.objects.get_or_create(
            email='ogrenci@example.com',
            defaults={
                'isim': 'Ali',
                'soyisim': 'Kaya',
                'rol': 'OGRENCI',
                'is_staff': False,
            }
        )
        ogrenci.set_password('12345678')
        ogrenci.save()

        # Yeni öğrenciler
        ogr2, _ = Kullanici.objects.get_or_create(
            email='ogrenci2@example.com',
            defaults={
                'isim': 'Zeynep',
                'soyisim': 'Demir',
                'rol': 'OGRENCI',
                'is_staff': False,
            }
        )
        ogr2.set_password('12345678')
        ogr2.save()

        ogr3, _ = Kullanici.objects.get_or_create(
            email='ogrenci3@example.com',
            defaults={
                'isim': 'Mehmet',
                'soyisim': 'Yıldız',
                'rol': 'OGRENCI',
                'is_staff': False,
            }
        )
        ogr3.set_password('12345678')
        ogr3.save()

        # Kurum oluştur
        kurum, _ = Kullanici.objects.get_or_create(
            email='kurum@example.com',
            defaults={
                'isim': 'Kurum Yetkili',
                'soyisim': 'Firma',
                'rol': 'KURUM',
                'is_staff': False,
            }
        )
        kurum.set_password('12345678')
        kurum.save()

        # Admin oluştur
        admin, _ = Kullanici.objects.get_or_create(
            email='admin@example.com',
            defaults={
                'isim': 'Admin',
                'soyisim': 'Yetkili',
                'rol': 'ADMIN',
                'is_staff': True,
                'is_superuser': True
            }
        )
        admin.set_password('12345678')
        admin.save()

        # Ortak kurum adı
        kurum_adi = 'ABC Yazılım'

        # Staj 1 - Ali Kaya
        staj1, _ = Staj.objects.get_or_create(
            ogrenci=ogrenci,
            kurum_adi=kurum_adi,
            baslangic_tarihi=timezone.now().date() - timedelta(days=10),
            bitis_tarihi=timezone.now().date() + timedelta(days=10),
            konu='Web tabanlı uygulama geliştirme',
            kurum_onaylandi=False,
        )

        # Staj Defteri - 3 günlük örnek
        for i in range(3):
            gun_tarihi = timezone.now().date() - timedelta(days=(2 - i))
            StajDefteri.objects.get_or_create(
                staj=staj1,
                gun_no=gun_tarihi,
                icerik=f"{gun_tarihi} - Python ve Django çalışmaları yapıldı."
            )

        # Staj 2 - Zeynep Demir
        Staj.objects.get_or_create(
            ogrenci=ogr2,
            kurum_adi=kurum_adi,
            baslangic_tarihi=date(2025, 7, 1),
            bitis_tarihi=date(2025, 7, 30),
            konu='Frontend geliştirme',
            kurum_onaylandi=True,
        )

        # Staj 3 - Mehmet Yıldız
        Staj.objects.get_or_create(
            ogrenci=ogr3,
            kurum_adi=kurum_adi,
            baslangic_tarihi=date(2025, 8, 1),
            bitis_tarihi=date(2025, 8, 30),
            konu='Veritabanı tasarımı',
            kurum_onaylandi=True,
        )

        self.stdout.write(self.style.SUCCESS('Test verileri (öğrenci, kurum, staj) başarıyla yüklendi.'))
