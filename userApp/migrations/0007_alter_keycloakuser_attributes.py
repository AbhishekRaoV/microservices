# Generated by Django 4.2.5 on 2023-10-11 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userApp', '0006_keycloakuser_attributes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keycloakuser',
            name='attributes',
            field=models.JSONField(),
        ),
    ]