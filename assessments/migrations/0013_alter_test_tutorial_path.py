# Generated by Django 3.2.8 on 2023-02-05 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessments', '0012_alter_test_tutorial_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='tutorial_path',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]