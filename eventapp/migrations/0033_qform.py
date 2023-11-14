# Generated by Django 3.2.16 on 2023-11-14 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventapp', '0032_ipsurl'),
    ]

    operations = [
        migrations.CreateModel(
            name='qform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_id', models.CharField(blank=True, max_length=255, null=True)),
                ('question', models.CharField(blank=True, max_length=255, null=True)),
                ('category', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
