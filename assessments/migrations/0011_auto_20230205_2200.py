# Generated by Django 3.2.8 on 2023-02-05 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessments', '0010_auto_20230205_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='psycometric',
            name='tutorial_path',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='test',
            name='tutorial_path',
            field=models.URLField(blank=True, null=True),
        ),
    ]
