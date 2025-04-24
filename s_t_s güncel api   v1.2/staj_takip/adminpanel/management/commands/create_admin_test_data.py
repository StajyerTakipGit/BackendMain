from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from staj.models import Staj
from faker import Faker
import random

fake = Faker(['tr_TR'])

class Command(BaseCommand):
    help = 'Admin panel test verileri oluşturur'

    def handle(self, *args, **options):
        self.stdout.write("Admin test verileri oluşturuluyor...")

        # Admin kullanıcı oluştur
        User = get_user_model()
        admin_user, created = User.objects.get_or_create(
            email='admin@universite.com',
            defaults={
                'isim': 'Admin',
                'soyisim': 'User',
                'is_staff': True,
                'is_superuser': True,
                'rol': 'admin',
                'is_active': True
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('Admin kullanıcı oluşturuldu'))

        # Öğrenci kullanıcılar oluştur
        students = []
        for i in range(10):
            student, created = User.objects.get_or_create(
                email=f'ogrenci{i}@universite.com',
                defaults={
                    'isim': fake.first_name(),
                    'soyisim': fake.last_name(),
                    'rol': 'ogrenci',
                    'is_active': True
                }
            )
            if created:
                student.set_password('ogrenci123')
                student.save()
            students.append(student)
        self.stdout.write(self.style.SUCCESS(f'{len(students)} öğrenci oluşturuldu'))

        # Stajlar oluştur (temel alanlarla)
        for i in range(20):
            student = random.choice(students)
            
            staj_data = {
                'ogrenci': student,
                'kurum_adi': fake.company(),
                'baslangic_tarihi': fake.date_between(start_date='-2y', end_date='-1y'),
                'bitis_tarihi': fake.date_between(start_date='-1y', end_date='today'),
            }

            # Sadece modelde tanımlı olan alanları ekleyelim
            try:
                staj = Staj.objects.create(**staj_data)
            except TypeError as e:
                self.stdout.write(self.style.ERROR(f'Hata oluştu: {e}'))
                self.stdout.write(self.style.ERROR('Staj modelinizin alanlarını kontrol edin.'))
                break

        self.stdout.write(self.style.SUCCESS(f'{Staj.objects.count()} staj kaydı oluşturuldu'))
        self.stdout.write(self.style.SUCCESS('Test verileri başarıyla oluşturuldu!'))