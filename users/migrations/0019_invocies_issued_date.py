# Generated by Django 3.2.18 on 2023-02-19 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_alter_invocies_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='invocies',
            name='issued_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
