from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator,RegexValidator
from django.utils import timezone

# Create your models here.
class DocketPDF(models.Model):
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
    
    def __str__(self) -> str:
        return str(self.docketNumber)

class WaitingTimeCost(models.Model):
    docketNo = models.ForeignKey(DocketPDF,on_delete=models.CASCADE)
    deliveryDate = models.DateField(default=timezone.now()) 
    source = models.CharField(max_length=255)   
    paidKMS = models.FloatField(default=0)
    invoiceQuantity = models.FloatField(default=0)
    unit = models.CharField(max_length=255)
    unitPrice = models.FloatField(default=0)
    TotalExGST = models.FloatField(default=0)
    GSTPayable = models.FloatField(default=0)
    TotalInGST = models.FloatField(default=0)
    
    def __str__(self) -> str:
        return str(self.TotalInGST)

class transferKMSCost(models.Model):
    docketNo = models.ForeignKey(DocketPDF,on_delete=models.CASCADE)
    deliveryDate = models.DateField(default=timezone.now())
    source = models.CharField(max_length=255)   
    paidKMS = models.FloatField(default=0)
    invoiceQuantity = models.FloatField(default=0)
    unit = models.CharField(max_length=255)
    unitPrice = models.FloatField(default=0)
    TotalExGST = models.FloatField(default=0)
    GSTPayable = models.FloatField(default=0)
    TotalInGST = models.FloatField(default=0)
    
    def __str__(self) -> str:
        return str(self.TotalInGST)
    
    


