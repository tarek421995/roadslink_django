# Generated by Django 3.2.18 on 2023-02-18 19:07

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20230218_1857'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='invocies',
            name='users_invoc_active_2721e4_idx',
        ),
        migrations.AlterField(
            model_name='invocies',
            name='users',
            field=models.ManyToManyField(blank=True, null=True, related_name='users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddIndex(
            model_name='invocies',
            index=models.Index(fields=['active', 'company', 'user', 'type', 'create_by', 'invocies_file', 'timestamp'], name='users_invoc_active_0ca011_idx'),
        ),
    ]
