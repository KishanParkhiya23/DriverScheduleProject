from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator,RegexValidator
from datetime import date
from django.utils import timezone

class Client(models.Model):
    clientId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    docketGiven = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(self.name)

class AdminTruck(models.Model):
    adminTruckNumber = models.PositiveIntegerField(validators=[MaxValueValidator(999999),MinValueValidator(100000)], unique=True)
    
    def __str__(self):
        return str(self.adminTruckNumber)
    
class ClientTruckConnection(models.Model):
    truckNumber = models.ForeignKey(AdminTruck, on_delete=models.CASCADE)
    clientId = models.ForeignKey(Client, on_delete=models.CASCADE)
    clientTruckId = models.PositiveIntegerField(validators=[MaxValueValidator(999999)],unique=True)
    # startDate = models.DateField(default=date.today())  
    startDate = models.DateField(default=timezone.now())  
    endDate = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.truckNumber) + str(self.clientId)
    
class Driver(models.Model):
    # driverId = models.IntegerField(primary_key=True, unique=True, default=generate_4digit_unique_key, editable=False)
    driverId = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=100, validators=[
        RegexValidator(
            regex=r'^\d{10}$',  # Match a 10-digit number
            message='Phone number must be a 10-digit number without any special characters or spaces.',
        ),
    ])
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=50)
    
    truckNum = models.ForeignKey(ClientTruckConnection, on_delete=models.CASCADE, default=None)

    def __str__(self) -> str:
        return str(self.driverId)
    

class LeaveRequest(models.Model):
    employee = models.ForeignKey(Driver, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Denied', 'Denied')], default='Pending')
    # Add other fields as needed

    def __str__(self):
        return f"{self.employee} - {self.start_date} to {self.end_date}"




class Source(models.Model):
    sourceName = models.CharField(primary_key=True, max_length=200)

    def __str__(self) -> str:
        return str(self.sourceName)

class Trip(models.Model):
    verified = models.BooleanField(default=False)
    driverId = models.ForeignKey(Driver, on_delete=models.CASCADE)
    clientName = models.CharField(max_length=200)
    shiftType = models.CharField(max_length=200)
    numberOfLoads = models.IntegerField()
    truckNo = models.IntegerField()
    shiftDate = models.DateTimeField()
    source = models.ForeignKey(Source, on_delete=models.PROTECT)
    startTime = models.CharField(max_length=200)
    endTime = models.CharField(max_length=200)
    logSheet = models.FileField(upload_to='static/img/finalLogSheet')
    comment = models.CharField(max_length=200)
    # dockets =  models.CharField(max_length=50)
    
    def __str__(self) -> str:
        return str(self.id)


class Docket(models.Model):
    docketId = models.AutoField(primary_key=True)
    tripId = models.ForeignKey(Trip, on_delete=models.CASCADE)
    docketNumber = models.IntegerField()
    # docketFile = models.CharField(max_length=200)
    docketFile = models.FileField(upload_to='static/img/docketFiles')

    def __str__(self) -> str:
        return str(self.tripId)





    
