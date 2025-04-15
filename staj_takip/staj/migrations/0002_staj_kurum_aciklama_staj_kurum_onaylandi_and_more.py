# Generated by Django 5.2 on 2025-04-14 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staj', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='staj',
            name='kurum_aciklama',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='staj',
            name='kurum_onaylandi',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='staj',
            name='kurum_puani',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
