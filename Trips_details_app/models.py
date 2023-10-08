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
    shiftDate = models.DateTimeField(null=True, default=None)
    startTime = models.CharField(max_length=200)
    endTime = models.CharField(max_length=200)
    logSheet = models.FileField(upload_to='static/img/finalLogSheet')
    comment = models.CharField(max_length=200, default='None')

    def __str__(self) -> str:
        return str(self.id)


class Docket(models.Model):
    docketId = models.AutoField(primary_key=True)
    tripId = models.ForeignKey(DriverTrip, on_delete=models.CASCADE)
    shiftDate = models.DateTimeField(null=True, default=None)
    docketNumber = models.IntegerField()
    docketFile = models.FileField(upload_to='static/img/docketFiles')
    basePlant = models.ForeignKey(BasePlant, on_delete=models.PROTECT)

    #  costs
    waitingTimeInMinutes = models.CharField(max_length=255)
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
        return self.waitingTimeCost + self.transferKMSCost + self.cubicMlCost + self.minLoadCost + self.othersCost

    def __str__(self) -> str:
        return str(self.tripId)

    class Meta:
        unique_together = (('docketNumber', 'shiftDate'),)

# category  ,call out  standby minute
# truck type ,replacement stand by slot


class PastTrip(models.Model):
    SHIFT_CHOICES = (
        ('Day', 'Day'),
        ('Night', 'Night'),
    )

    Date = models.DateTimeField(null=True, default=None)
    Truck_No = models.CharField(max_length=255, null=True, default=None)
    Truck_Type = models.CharField(max_length=255, null=True, default=None)
    Replacement = models.CharField(max_length=255, null=True, default=None)
    Driver_Name = models.CharField(max_length=255, null=True, default=None)
    Docket_NO = models.CharField(max_length=255, null=True, default=None)
    Load_Time = models.DateTimeField(null=True, default=None)
    Return_time = models.DateTimeField(null=True, default=None)
    Load_qty = models.PositiveIntegerField(null=True, default=None)
    Doc_KMs = models.FloatField(null=True, default=None)
    Actual_KMs = models.FloatField(null=True, default=None)
    waiting_time_starts_Onsite = models.DateTimeField(null=True, default=None)
    waiting_time_end_offsite = models.DateTimeField(null=True, default=None)
    Total_minutes = models.IntegerField(null=True, default=None)
    Returned_Qty = models.PositiveIntegerField(null=True, default=None)
    Returned_KM = models.FloatField(null=True, default=None)
    Returned_to_Yard = models.BooleanField(null=True, default=None)
    Comment = models.TextField(null=True, default=None)
    Transfer_KM = models.FloatField(null=True, default=None)
    stand_by_Start_Time = models.DateTimeField(null=True, default=None)
    stand_by_end_time = models.DateTimeField(null=True, default=None)
    stand_by_total_minute = models.IntegerField(null=True, default=None)
    Stand_by_slot = models.CharField(max_length=255, null=True, default=None)
    category = models.CharField(max_length=255, null=True, default=None)
    call_out = models.CharField(max_length=255, null=True, default=None)
    standby_minute = models.IntegerField(null=True, default=None)
    ShiftType = models.CharField(max_length=5, choices=SHIFT_CHOICES, null=True, default=None)


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
    Staff_Notes = models.CharField(max_length=1024)

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
# RCTA
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
    docketNo = models.ForeignKey(ClientTrip, on_delete=models.CASCADE)
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
    docketNo = models.ForeignKey(ClientTrip, on_delete=models.CASCADE)
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
