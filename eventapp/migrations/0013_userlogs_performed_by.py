# Generated by Django 3.2.16 on 2023-10-09 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventapp', '0012_userlogs'),
    ]

    operations = [
        migrations.AddField(
            model_name='userlogs',
            name='performed_by',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]