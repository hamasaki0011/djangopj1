# Generated by Django 3.2.17 on 2023-02-16 06:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_location_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='location',
            options={'verbose_name': '現場', 'verbose_name_plural': '現場一覧'},
        ),
    ]
