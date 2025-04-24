from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class KullaniciYonetici(BaseUserManager):
    def create_user(self, email, isim, soyisim, password=None, rol='OGRENCI'):
        if not email:
            raise ValueError('Email zorunludur')
        email = self.normalize_email(email)
        user = self.model(email=email, isim=isim, soyisim=soyisim, rol=rol)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, isim, soyisim, password):
        user = self.create_user(email, isim, soyisim, password, rol='ADMIN')
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class Kullanici(AbstractBaseUser, PermissionsMixin):
    ROL_SECENEKLERI = [
        ('OGRENCI', 'Öğrenci'),
        ('KURUM', 'Kurum'),
        ('ADMIN', 'Admin'),
    ]

    email = models.EmailField(unique=True)
    isim = models.CharField(max_length=50)
    soyisim = models.CharField(max_length=50)
    rol = models.CharField(max_length=10, choices=ROL_SECENEKLERI, default='OGRENCI')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = KullaniciYonetici()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['isim', 'soyisim']

    def __str__(self):
        return f"{self.email} ({self.rol})"