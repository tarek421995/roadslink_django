# Generated by Django 3.2.18 on 2023-02-19 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_invocies_issued_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invocies',
            name='end_date',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='invocies',
            name='start_date',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
