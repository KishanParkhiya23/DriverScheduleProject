from django.db import models
from django.utils import timezone
from Basic_app.models import *
    

class DriverTrip(models.Model):
    verified = models.BooleanField(default=False)
    driverId = models.ForeignKey(Driver, on_delete=models.CASCADE)
    clientName = models.CharField(max_length=200)
    shiftType = models.CharField(max_length=200)
    numberOfLoads = models.IntegerField()
    truckNo = models.IntegerField()
    shiftDate = models.DateTimeField()
    basePlant = models.ForeignKey(BasePlant, on_delete=models.PROTECT)
    startTime = models.CharField(max_length=200)
    endTime = models.CharField(max_length=200)
    logSheet = models.FileField(upload_to='static/img/finalLogSheet')
    comment = models.CharField(max_length=200)
    
    def __str__(self) -> str:
        return str(self.id)


class Docket(models.Model):
    docketId = models.AutoField(primary_key=True)
    tripId = models.ForeignKey(DriverTrip, on_delete=models.CASCADE)
    docketNumber = models.IntegerField()
    docketFile = models.FileField(upload_to='static/img/docketFiles')
    #  costs
    waitingTime = models.TimeField(default=timezone.now())
    waitingTimeCost = models.FloatField(default=0)
    
    transferKMS = models.PositiveIntegerField(default=0)
    transferKMSCost = models.FloatField(default=0)
    
    cubicMl = models.PositiveIntegerField(default=0)
    cubicMlCost = models.FloatField(default=0)
    
    minLoad = models.PositiveIntegerField(default=0)
    minLoadCost = models.FloatField(default=0)
    
    others = models.PositiveIntegerField(default=0)
    othersCost = models.FloatField(default=0)
    
    @property
    def total_cost(self):
        print("Cost")
        return self.waitingTimeCost + self.transferKMSCost + self.cubicMlCost + self.minLoadCost + self.othersCost
    
    def __str__(self) -> str:
        return str(self.tripId)


class Appointment(models.Model):
    TRIP_STATUS = [
        ('unassigned', 'Unassigned'),
        ('assigned', 'Assigned'),
        ('dispacted', 'Dispatched'),
        ('in_progress', 'In Progress'),
        ('incomplete', 'Incomplete'),
        ('complete', 'Complete'),
        ('cancelled', 'Cancelled'),
    ]
    scheduled = models.BooleanField(default=False)

    Title = models.CharField(max_length=255)
    Start_Date_Time = models.DateTimeField(default=timezone.now())
    End_Date_Time = models.DateTimeField(default=timezone.now())
    report_to_origin = models.DateTimeField(default=timezone.now())
    Status = models.CharField(
        max_length=20, choices=TRIP_STATUS, default='incomplete'
    )
    Origin = models.CharField(max_length=255)
    Recurring = models.CharField(max_length=255)
    Staff_Notes	= models.CharField(max_length=1024)
    
    Created_by = models.CharField(max_length=255)
    Created_time = models.TimeField(auto_now=True)

    Report_Time = models.TimeField()
    Dwell_Time = models.TimeField()
    Block_Time = models.TimeField()
    Total_Time = models.TimeField()

    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    stop = models.ForeignKey(Client, on_delete=models.CASCADE)


    def is_driver_available(self):
        leave_requests = self.driver.leaverequest_set.filter(
            start_date__lte=self.Start_Date_Time,
            end_date__gte=self.Start_Date_Time,
            status='Approved'
        )
        return not leave_requests.exists()


# Create your models here.
class ClientTrip(models.Model):
    docketNumber = models.IntegerField()
    truckNo = models.FloatField(default=0)
    #  costs
    # waitingTime = models.TimeField(default=timezone.now())
    # waitingTimeCost = models.FloatField(default=0)
    
    # transferKMS = models.PositiveIntegerField(default=0)
    # transferKMSCost = models.FloatField(default=0)
    
    # cubicMl = models.PositiveIntegerField(default=0)
    # cubicMlCost = models.FloatField(default=0)
    
    # minLoad = models.PositiveIntegerField(default=0)
    # minLoadCost = models.FloatField(default=0)
    
    # others = models.PositiveIntegerField(default=0)
    # othersCost = models.FloatField(default=0)
    
    # @property
    # def total_cost(self):
    #     print("Cost")
    #     return self.waitingTimeCost + self.transferKMSCost + self.cubicMlCost + self.minLoadCost + self.othersCost
    
    def _str_(self) -> str:
        return str(self.docketNumber) + str(self.truckNo)

class WaitingTimeCost(models.Model):
    docketNo = models.ForeignKey(ClientTrip,on_delete=models.CASCADE)
    deliveryDate = models.DateField(default=timezone.now()) 
    basePlant = models.CharField(max_length=255)   
    paidKMS = models.FloatField(default=0)
    invoiceQuantity = models.FloatField(default=0)
    unit = models.CharField(max_length=255)
    unitPrice = models.FloatField(default=0)
    TotalExGST = models.FloatField(default=0)
    GSTPayable = models.FloatField(default=0)
    TotalInGST = models.FloatField(default=0)
    
    def _str_(self) -> str:
        return str(self.TotalInGST)

class transferKMSCost(models.Model):
    docketNo = models.ForeignKey(ClientTrip,on_delete=models.CASCADE)
    deliveryDate = models.DateField(default=timezone.now())
    basePlant = models.CharField(max_length=255)   
    paidKMS = models.FloatField(default=0)
    invoiceQuantity = models.FloatField(default=0)
    unit = models.CharField(max_length=255)
    unitPrice = models.FloatField(default=0)
    TotalExGST = models.FloatField(default=0)
    GSTPayable = models.FloatField(default=0)
    TotalInGST = models.FloatField(default=0)
    
    def _str_(self) -> str:
        return str(self.TotalInGST)
