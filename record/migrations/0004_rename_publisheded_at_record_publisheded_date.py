# Generated by Django 3.2.17 on 2023-02-07 02:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('record', '0003_rename_puvlisheded_at_record_publisheded_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='record',
            old_name='publisheded_at',
            new_name='publisheded_date',
        ),
    ]
