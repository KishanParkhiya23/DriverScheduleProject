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
    
    def __str__(self) -> str:
        return str(self.driverId) + str(self.name)


class ClientTruckConnection(models.Model):
    truckNumber = models.ForeignKey(AdminTruck, on_delete=models.CASCADE)
    clientId = models.ForeignKey(Client, on_delete=models.CASCADE)
    driverId =  models.ForeignKey(Driver, on_delete=models.CASCADE)
    clientTruckId = models.PositiveIntegerField(validators=[MaxValueValidator(999999)],unique=True)
    # startDate = models.DateField(default=date.today())  
    startDate = models.DateField(default=timezone.now())  
    endDate = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.truckNumber) + str(self.clientId)


class BasePlant(models.Model):
    basePlant = models.CharField(primary_key=True, max_length=200)

    def __str__(self) -> str:
        return str(self.basePlant)


class Cost(models.Model):
    is_Active = models.BooleanField(default=True)
    cost_id = models.PositiveBigIntegerField(primary_key=True)
    clientId = models.ForeignKey(Client,on_delete=models.CASCADE)
    basePlant = models.ForeignKey(BasePlant,on_delete=models.CASCADE)
    truck_number = models.ForeignKey(AdminTruck ,on_delete=models.CASCADE)
    startDate = models.DateField(default=timezone.now())  
    endDate = models.DateField(null=True, blank=True)
    transferKMSCost = models.FloatField(default=0)
    waitingTimeCost = models.FloatField(default=0)
    cartagePerCumCost = models.FloatField(default=0)
    surchargeCost = models.FloatField(default=0)
    
    def __str__(self) -> str:
        return str(self.cost_id) + str(self.clientId) + str(self.basePlant)
