# Generated by Django 4.2.5 on 2023-10-11 07:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('userApp', '0005_keycloakuser_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='keycloakuser',
            name='attributes',
            field=models.JSONField(default=django.utils.timezone.now, verbose_name='attributes'),
            preserve_default=False,
        ),
    ]
