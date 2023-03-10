# Generated by Django 4.1.3 on 2023-02-16 12:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dashboard', '0001_initial'),
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.author'),
        ),
        migrations.AddField(
            model_name='blog',
            name='catagories',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='blog.catagory'),
        ),
        migrations.AddField(
            model_name='blog',
            name='tags',
            field=models.ManyToManyField(blank=True, to='blog.tag'),
        ),
    ]
