# Generated by Django 4.2.1 on 2023-10-02 04:07

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminTruck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adminTruckNumber', models.PositiveIntegerField(unique=True, validators=[django.core.validators.MaxValueValidator(999999), django.core.validators.MinValueValidator(100000)])),
            ],
        ),
        migrations.CreateModel(
            name='BasePlant',
            fields=[
                ('basePlant', models.CharField(max_length=200, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('clientId', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('docketGiven', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('driverId', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=100, validators=[django.core.validators.RegexValidator(message='Phone number must be a 10-digit number without any special characters or spaces.', regex='^\\d{10}$')])),
                ('email', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Cost',
            fields=[
                ('is_Active', models.BooleanField(default=True)),
                ('cost_id', models.PositiveBigIntegerField(primary_key=True, serialize=False)),
                ('startDate', models.DateField(default=datetime.datetime(2023, 10, 2, 4, 7, 37, 320359, tzinfo=datetime.timezone.utc))),
                ('endDate', models.DateField(blank=True, null=True)),
                ('transferKMSCost', models.FloatField(default=0)),
                ('waitingTimeCost', models.FloatField(default=0)),
                ('cartagePerCumCost', models.FloatField(default=0)),
                ('surchargeCost', models.FloatField(default=0)),
                ('basePlant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Basic_app.baseplant')),
                ('clientId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Basic_app.client')),
                ('truck_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Basic_app.admintruck')),
            ],
        ),
        migrations.CreateModel(
            name='ClientTruckConnection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clientTruckId', models.PositiveIntegerField(unique=True, validators=[django.core.validators.MaxValueValidator(999999)])),
                ('startDate', models.DateField(default=datetime.datetime(2023, 10, 2, 4, 7, 37, 319361, tzinfo=datetime.timezone.utc))),
                ('endDate', models.DateField(blank=True, null=True)),
                ('clientId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Basic_app.client')),
                ('driverId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Basic_app.driver')),
                ('truckNumber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Basic_app.admintruck')),
            ],
        ),
    ]
