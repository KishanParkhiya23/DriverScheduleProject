# Generated by Django 4.2.1 on 2023-09-09 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DriverSchedule_app', '0004_leaverequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaverequest',
            name='end_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='leaverequest',
            name='start_date',
            field=models.DateTimeField(),
        ),
    ]
