# Generated by Django 4.2.1 on 2023-09-30 10:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Invoice_analysis_app', '0002_alter_transferkmscost_deliverydate_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transferkmscost',
            name='docketNo',
        ),
        migrations.RemoveField(
            model_name='waitingtimecost',
            name='docketNo',
        ),
        migrations.DeleteModel(
            name='DocketPDF',
        ),
        migrations.DeleteModel(
            name='transferKMSCost',
        ),
        migrations.DeleteModel(
            name='WaitingTimeCost',
        ),
    ]
