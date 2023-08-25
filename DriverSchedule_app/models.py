from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# def generate_4digit_unique_key():
#     try:
#         latest_data = Driver.objects.latest('Uniqeid')
#         latest_data = int(latest_data.Uniqeid)
#         random = latest_data+1
#     except:
#         random =  1111
#     return random


class Driver(models.Model):
    # driverId = models.IntegerField(primary_key=True, unique=True, default=generate_4digit_unique_key, editable=False)
    driverId = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=50)

    def __str__(self) -> str:
        return str(self.driverId)


class Client(models.Model):
    clientId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return str(self.name)


class Source(models.Model):

    sourceName = models.CharField(primary_key=True, max_length=200)

    def __str__(self) -> str:
        return str(self.sourceName)


class Trip(models.Model):
    driverId = models.ForeignKey(Driver, on_delete=models.CASCADE)
    clientName = models.CharField(max_length=200)
    shiftType = models.CharField(max_length=200)
    numberOfLog = models.IntegerField()
    truckNo = models.IntegerField()
    shiftDate = models.DateTimeField()
    source = models.ForeignKey(Source, on_delete=models.PROTECT)
    startTime = models.CharField(max_length=200)
    endTime = models.CharField(max_length=200)
    logSheet = models.CharField(max_length=200)
    comment = models.CharField(max_length=200)

    def __str__(self) -> str:
        return str(self.id)


class Docket(models.Model):
    docketId = models.AutoField(primary_key=True)
    tripId = models.ForeignKey(Trip, on_delete=models.CASCADE)
    docketNumber = models.IntegerField()
    docketFile = models.CharField(max_length=200)

    def __str__(self) -> str:
        return str(self.tripId)


class AdminTruck(models.Model):
    adminTruckNumber = models.PositiveIntegerField(
        validators=[MaxValueValidator(99999), MinValueValidator(10000)], unique=True)
    
    def __str__(self):
        return str(self.adminTruckNumber)


class ClientTruckConnection(models.Model):
    truckNumber = models.ForeignKey(AdminTruck, on_delete=models.CASCADE)
    clientId = models.ForeignKey(Client, on_delete=models.CASCADE)
    clientTruckId = models.PositiveIntegerField(primary_key=True, validators=[
                                                MaxValueValidator(999999), MinValueValidator(100000)])

    def __str__(self):
        return str(self.truckNumber) + str(self.clientId)
