# Generated by Django 3.2.16 on 2023-12-01 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventapp', '0037_rename_quest2ion_qform_question'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ecert',
            name='q1',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
        migrations.AlterField(
            model_name='ecert',
            name='q2',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
        migrations.AlterField(
            model_name='ecert',
            name='q3',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
        migrations.AlterField(
            model_name='ecert',
            name='q4',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]
