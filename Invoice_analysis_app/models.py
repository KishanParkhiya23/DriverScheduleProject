from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator,RegexValidator
from django.utils import timezone

# Create your models here.


class DocketPDF(models.Model):
    docketId = models.AutoField(primary_key=True)
    docketNumber = models.IntegerField()
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
