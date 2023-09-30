# Generated by Django 4.2.1 on 2023-09-30 09:58

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DocketPDF',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('docketNumber', models.IntegerField()),
                ('truckNo', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='WaitingTimeCost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deliveryDate', models.DateField(default=datetime.datetime(2023, 9, 30, 9, 58, 0, 417193, tzinfo=datetime.timezone.utc))),
                ('basePlant', models.CharField(max_length=255)),
                ('paidKMS', models.FloatField(default=0)),
                ('invoiceQuantity', models.FloatField(default=0)),
                ('unit', models.CharField(max_length=255)),
                ('unitPrice', models.FloatField(default=0)),
                ('TotalExGST', models.FloatField(default=0)),
                ('GSTPayable', models.FloatField(default=0)),
                ('TotalInGST', models.FloatField(default=0)),
                ('docketNo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Invoice_analysis_app.docketpdf')),
            ],
        ),
        migrations.CreateModel(
            name='transferKMSCost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deliveryDate', models.DateField(default=datetime.datetime(2023, 9, 30, 9, 58, 0, 419187, tzinfo=datetime.timezone.utc))),
                ('basePlant', models.CharField(max_length=255)),
                ('paidKMS', models.FloatField(default=0)),
                ('invoiceQuantity', models.FloatField(default=0)),
                ('unit', models.CharField(max_length=255)),
                ('unitPrice', models.FloatField(default=0)),
                ('TotalExGST', models.FloatField(default=0)),
                ('GSTPayable', models.FloatField(default=0)),
                ('TotalInGST', models.FloatField(default=0)),
                ('docketNo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Invoice_analysis_app.docketpdf')),
            ],
        ),
    ]
