# Generated by Django 3.2.17 on 2023-02-08 05:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='作成日'),
        ),
        migrations.AlterField(
            model_name='location',
            name='updated_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='更新日'),
        ),
    ]
