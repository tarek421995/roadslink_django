# Generated by Django 3.2.18 on 2023-02-18 20:04

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_alter_invocies_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invocies',
            name='users',
            field=models.ManyToManyField(blank=True, related_name='users', to=settings.AUTH_USER_MODEL),
        ),
    ]
