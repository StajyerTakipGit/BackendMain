from django.core.management.base import BaseCommand
from kullanici.models import Kullanici
from staj.models import Staj, StajDefteri
from django.utils import timezone
from datetime import timedelta

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

        # Staj oluştur
        staj, _ = Staj.objects.get_or_create(
            ogrenci=ogrenci,
            kurum_adi='ABC Yazılım',
            baslangic_tarihi=timezone.now().date() - timedelta(days=10),
            bitis_tarihi=timezone.now().date() + timedelta(days=10),
            konu='Web tabanlı uygulama geliştirme',
            kurum_onaylandi=False,
        )

        # Staj Defteri - 3 günlük örnek
        for i in range(1, 4):
            StajDefteri.objects.get_or_create(
                staj=staj,
                gun_no=i,
                icerik=f"{i}. gün - Python ve Django çalışmaları yapıldı."
            )

        self.stdout.write(self.style.SUCCESS('Test verileri başarıyla yüklendi.'))