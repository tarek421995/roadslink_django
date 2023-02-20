# Generated by Django 3.2.18 on 2023-02-18 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_cretificate_user'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='cretificate',
            name='users_creti_user_id_94c325_idx',
        ),
        migrations.AddIndex(
            model_name='cretificate',
            index=models.Index(fields=['user', 'final_en_score', 'company', 'final_psyco_score', 'timestamp', 'created_at'], name='users_creti_user_id_c7c85a_idx'),
        ),
    ]
