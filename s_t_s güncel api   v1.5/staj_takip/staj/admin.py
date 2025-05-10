from django.contrib import admin

from .models import HesapTalep

@admin.register(HesapTalep)
class HesapTalepAdmin(admin.ModelAdmin):
    list_display = ('email', 'isim', 'rol', 'onaylandi', 'tarih')
    list_filter = ('rol', 'onaylandi')
    search_fields = ('email', 'isim')
