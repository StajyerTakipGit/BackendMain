from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

class Command(BaseCommand):
    help = 'Token almak için test kullanıcısı oluşturur'

    def handle(self, *args, **options):
        # Test kullanıcısını email üzerinden oluştur
        test_user, created = User.objects.get_or_create(
            email='test@example.com',
            defaults={
                'isim': 'Test',
                'soyisim': 'User',
                'password': 'testpassword123',
                'rol': 'OGRENCI'  # Modelinize göre bu alan gerekli olabilir
            }
        )

        if created:
            test_user.set_password('testpassword123')
            test_user.save()
            # Token oluştur
            Token.objects.create(user=test_user)
            self.stdout.write(
                self.style.SUCCESS('Test kullanıcısı oluşturuldu:\n'
                                  f'Email: test@example.com\n'
                                  f'Password: testpassword123')
            )
        else:
            self.stdout.write(self.style.WARNING('Test kullanıcısı zaten mevcut'))

        # Token ile giriş testi için bilgileri göster
        self.stdout.write(
            self.style.SUCCESS('\nToken almak için POST isteği örneği:\n'
                              'URL: http://localhost:8000/api/giris/\n'
                              'Headers: {"Content-Type": "application/json"}\n'
                              'Body: {"email": "test@example.com", "password": "testpassword123"}')
        )