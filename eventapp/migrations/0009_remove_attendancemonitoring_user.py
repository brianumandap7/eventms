# Generated by Django 3.2.16 on 2023-10-06 01:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventapp', '0008_attendancemonitoring_time_in'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendancemonitoring',
            name='user',
        ),
    ]
