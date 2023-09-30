# Generated by Django 4.2.1 on 2023-09-30 05:50

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
            name='NatureOfLeave',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('verified', models.BooleanField(default=False)),
                ('clientName', models.CharField(max_length=200)),
                ('shiftType', models.CharField(max_length=200)),
                ('numberOfLoads', models.IntegerField()),
                ('truckNo', models.IntegerField()),
                ('shiftDate', models.DateTimeField()),
                ('startTime', models.CharField(max_length=200)),
                ('endTime', models.CharField(max_length=200)),
                ('logSheet', models.FileField(upload_to='static/img/finalLogSheet')),
                ('comment', models.CharField(max_length=200)),
                ('basePlant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='DriverSchedule_app.baseplant')),
                ('driverId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DriverSchedule_app.driver')),
            ],
        ),
        migrations.CreateModel(
            name='LeaveRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Denied', 'Denied')], default='Pending', max_length=20)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DriverSchedule_app.driver')),
                ('reason', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DriverSchedule_app.natureofleave')),
            ],
        ),
        migrations.CreateModel(
            name='Docket',
            fields=[
                ('docketId', models.AutoField(primary_key=True, serialize=False)),
                ('docketNumber', models.IntegerField()),
                ('docketFile', models.FileField(upload_to='static/img/docketFiles')),
                ('waitingTime', models.TimeField(default=datetime.datetime(2023, 9, 30, 5, 49, 56, 464981, tzinfo=datetime.timezone.utc))),
                ('waitingTimeCost', models.FloatField(default=0)),
                ('transferKMS', models.PositiveIntegerField(default=0)),
                ('transferKMSCost', models.FloatField(default=0)),
                ('cubicMl', models.PositiveIntegerField(default=0)),
                ('cubicMlCost', models.FloatField(default=0)),
                ('minLoad', models.PositiveIntegerField(default=0)),
                ('minLoadCost', models.FloatField(default=0)),
                ('others', models.PositiveIntegerField(default=0)),
                ('othersCost', models.FloatField(default=0)),
                ('tripId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DriverSchedule_app.trip')),
            ],
        ),
        migrations.CreateModel(
            name='Cost',
            fields=[
                ('is_Active', models.BooleanField(default=True)),
                ('cost_id', models.PositiveBigIntegerField(primary_key=True, serialize=False)),
                ('startDate', models.DateField(default=datetime.datetime(2023, 9, 30, 5, 49, 56, 467969, tzinfo=datetime.timezone.utc))),
                ('endDate', models.DateField(blank=True, null=True)),
                ('transferKMSCost', models.FloatField(default=0)),
                ('waitingTimeCost', models.FloatField(default=0)),
                ('cartagePerCumCost', models.FloatField(default=0)),
                ('surchargeCost', models.FloatField(default=0)),
                ('basePlant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DriverSchedule_app.baseplant')),
                ('clientId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DriverSchedule_app.client')),
                ('truck_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DriverSchedule_app.admintruck')),
            ],
        ),
        migrations.CreateModel(
            name='ClientTruckConnection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clientTruckId', models.PositiveIntegerField(unique=True, validators=[django.core.validators.MaxValueValidator(999999)])),
                ('startDate', models.DateField(default=datetime.datetime(2023, 9, 30, 5, 49, 56, 456943, tzinfo=datetime.timezone.utc))),
                ('endDate', models.DateField(blank=True, null=True)),
                ('clientId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DriverSchedule_app.client')),
                ('driverId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DriverSchedule_app.driver')),
                ('truckNumber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DriverSchedule_app.admintruck')),
            ],
        ),
    ]
