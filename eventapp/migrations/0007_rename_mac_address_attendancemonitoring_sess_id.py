# Generated by Django 3.2.16 on 2023-10-06 00:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventapp', '0006_attendancemonitoring'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attendancemonitoring',
            old_name='mac_address',
            new_name='sess_id',
        ),
    ]