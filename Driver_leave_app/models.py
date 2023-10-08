from django.db import models
from Basic_app.models import *


class NatureOfLeave(models.Model):
    reason = models.CharField(max_length=200)
    
    def __str__(self) -> str:
            return str(self.reason)


class LeaveRequest(models.Model):
    employee = models.ForeignKey(Driver, on_delete=models.CASCADE)
    start_date = models.DateTimeField(null=True, default=None)
    end_date = models.DateTimeField(null=True, default=None)
    reason = models.ForeignKey(NatureOfLeave,on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Denied', 'Denied')], default='Pending')
    # Add other fields as needed

    def __str__(self):
        return f"{self.employee} - {self.start_date} to {self.end_date}"

