# Generated by Django 3.2.16 on 2023-10-06 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventapp', '0007_rename_mac_address_attendancemonitoring_sess_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendancemonitoring',
            name='time_in',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]