# Generated by Django 3.2.16 on 2023-10-13 06:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventapp', '0018_delete_userchangelog'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalevents_details',
            name='events_requestor',
        ),
        migrations.RemoveField(
            model_name='historicalevents_details',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicaluserlogs',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicaluserprofile',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicaluserprofile',
            name='user',
        ),
        migrations.DeleteModel(
            name='HistoricalAttendanceMonitoring',
        ),
        migrations.DeleteModel(
            name='Historicalevents_details',
        ),
        migrations.DeleteModel(
            name='HistoricalUserLogs',
        ),
        migrations.DeleteModel(
            name='HistoricalUserProfile',
        ),
    ]