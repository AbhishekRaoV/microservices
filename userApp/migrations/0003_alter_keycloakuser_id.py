# Generated by Django 4.2.5 on 2023-09-20 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userApp', '0002_alter_keycloakuser_createdtimestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keycloakuser',
            name='id',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
    ]