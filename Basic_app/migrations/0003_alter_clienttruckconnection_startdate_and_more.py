# Generated by Django 4.2.1 on 2023-10-04 11:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Basic_app', '0002_alter_clienttruckconnection_startdate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clienttruckconnection',
            name='startDate',
            field=models.DateField(default=datetime.datetime(2023, 10, 4, 11, 36, 22, 591343, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='cost',
            name='startDate',
            field=models.DateField(default=datetime.datetime(2023, 10, 4, 11, 36, 22, 592340, tzinfo=datetime.timezone.utc)),
        ),
    ]
