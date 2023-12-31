# Generated by Django 4.2.1 on 2023-10-04 11:36

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Basic_app', '0003_alter_clienttruckconnection_startdate_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientTrip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('docketNumber', models.IntegerField()),
                ('truckNo', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='PastTrip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date', models.DateTimeField(default=None, null=True)),
                ('Truck_No', models.CharField(default=None, max_length=255, null=True)),
                ('Truck_Type', models.CharField(default=None, max_length=255, null=True)),
                ('Replacement', models.CharField(default=None, max_length=255, null=True)),
                ('Driver_Name', models.CharField(default=None, max_length=255, null=True)),
                ('Docket_NO', models.CharField(default=None, max_length=255, null=True)),
                ('Load_Time', models.DateTimeField(default=None, null=True)),
                ('Return_time', models.DateTimeField(default=None, null=True)),
                ('Load_qty', models.PositiveIntegerField(default=None, null=True)),
                ('Doc_KMs', models.FloatField(default=None, null=True)),
                ('Actual_KMs', models.FloatField(default=None, null=True)),
                ('waiting_time_starts_Onsite', models.DateTimeField(default=None, null=True)),
                ('waiting_time_end_offsite', models.DateTimeField(default=None, null=True)),
                ('Total_minutes', models.IntegerField(default=None, null=True)),
                ('Returned_Qty', models.PositiveIntegerField(default=None, null=True)),
                ('Returned_KM', models.FloatField(default=None, null=True)),
                ('Returned_to_Yard', models.BooleanField(default=None, null=True)),
                ('Comment', models.TextField(default=None, null=True)),
                ('Transfer_KM', models.FloatField(default=None, null=True)),
                ('stand_by_Start_Time', models.DateTimeField(default=None, null=True)),
                ('stand_by_end_time', models.DateTimeField(default=None, null=True)),
                ('stand_by_total_minute', models.IntegerField(default=None, null=True)),
                ('Stand_by_slot', models.CharField(default=None, max_length=255, null=True)),
                ('category', models.CharField(default=None, max_length=255, null=True)),
                ('call_out', models.CharField(default=None, max_length=255, null=True)),
                ('standby_minute', models.IntegerField(default=None, null=True)),
                ('ShiftType', models.CharField(choices=[('Day', 'Day'), ('Night', 'Night')], default=None, max_length=5, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='WaitingTimeCost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deliveryDate', models.DateField(default=datetime.datetime(2023, 10, 4, 11, 36, 22, 597327, tzinfo=datetime.timezone.utc))),
                ('basePlant', models.CharField(max_length=255)),
                ('paidKMS', models.FloatField(default=0)),
                ('invoiceQuantity', models.FloatField(default=0)),
                ('unit', models.CharField(max_length=255)),
                ('unitPrice', models.FloatField(default=0)),
                ('TotalExGST', models.FloatField(default=0)),
                ('GSTPayable', models.FloatField(default=0)),
                ('TotalInGST', models.FloatField(default=0)),
                ('docketNo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Trips_details_app.clienttrip')),
            ],
        ),
        migrations.CreateModel(
            name='transferKMSCost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deliveryDate', models.DateField(default=datetime.datetime(2023, 10, 4, 11, 36, 22, 597327, tzinfo=datetime.timezone.utc))),
                ('basePlant', models.CharField(max_length=255)),
                ('paidKMS', models.FloatField(default=0)),
                ('invoiceQuantity', models.FloatField(default=0)),
                ('unit', models.CharField(max_length=255)),
                ('unitPrice', models.FloatField(default=0)),
                ('TotalExGST', models.FloatField(default=0)),
                ('GSTPayable', models.FloatField(default=0)),
                ('TotalInGST', models.FloatField(default=0)),
                ('docketNo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Trips_details_app.clienttrip')),
            ],
        ),
        migrations.CreateModel(
            name='DriverTrip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('verified', models.BooleanField(default=False)),
                ('clientName', models.CharField(max_length=200)),
                ('shiftType', models.CharField(max_length=200)),
                ('numberOfLoads', models.IntegerField()),
                ('truckNo', models.IntegerField()),
                ('shiftDate', models.DateTimeField(default=None, null=True)),
                ('startTime', models.CharField(max_length=200)),
                ('endTime', models.CharField(max_length=200)),
                ('logSheet', models.FileField(upload_to='static/img/finalLogSheet')),
                ('comment', models.CharField(default='None', max_length=200)),
                ('driverId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Basic_app.driver')),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scheduled', models.BooleanField(default=False)),
                ('Title', models.CharField(max_length=255)),
                ('Start_Date_Time', models.DateTimeField(default=datetime.datetime(2023, 10, 4, 11, 36, 22, 596329, tzinfo=datetime.timezone.utc))),
                ('End_Date_Time', models.DateTimeField(default=datetime.datetime(2023, 10, 4, 11, 36, 22, 596329, tzinfo=datetime.timezone.utc))),
                ('report_to_origin', models.DateTimeField(default=datetime.datetime(2023, 10, 4, 11, 36, 22, 596329, tzinfo=datetime.timezone.utc))),
                ('Status', models.CharField(choices=[('unassigned', 'Unassigned'), ('assigned', 'Assigned'), ('dispacted', 'Dispatched'), ('in_progress', 'In Progress'), ('incomplete', 'Incomplete'), ('complete', 'Complete'), ('cancelled', 'Cancelled')], default='incomplete', max_length=20)),
                ('Origin', models.CharField(max_length=255)),
                ('Recurring', models.CharField(max_length=255)),
                ('Staff_Notes', models.CharField(max_length=1024)),
                ('Created_by', models.CharField(max_length=255)),
                ('Created_time', models.TimeField(auto_now=True)),
                ('Report_Time', models.TimeField()),
                ('Dwell_Time', models.TimeField()),
                ('Block_Time', models.TimeField()),
                ('Total_Time', models.TimeField()),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Basic_app.driver')),
                ('stop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Basic_app.client')),
            ],
        ),
        migrations.CreateModel(
            name='Docket',
            fields=[
                ('docketId', models.AutoField(primary_key=True, serialize=False)),
                ('shiftDate', models.DateTimeField(default=None, null=True)),
                ('docketNumber', models.IntegerField()),
                ('docketFile', models.FileField(upload_to='static/img/docketFiles')),
                ('waitingTimeInMinutes', models.CharField(max_length=255)),
                ('waitingTimeCost', models.FloatField(default=0)),
                ('transferKMS', models.PositiveIntegerField(default=0)),
                ('transferKMSCost', models.FloatField(default=0)),
                ('cubicMl', models.PositiveIntegerField(default=0)),
                ('cubicMlCost', models.FloatField(default=0)),
                ('minLoad', models.PositiveIntegerField(default=0)),
                ('minLoadCost', models.FloatField(default=0)),
                ('others', models.PositiveIntegerField(default=0)),
                ('othersCost', models.FloatField(default=0)),
                ('basePlant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Basic_app.baseplant')),
                ('tripId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Trips_details_app.drivertrip')),
            ],
            options={
                'unique_together': {('docketNumber', 'shiftDate')},
            },
        ),
    ]
