from django.db import models
from accounts.models import User
# Create your models here.

class IrrigationSchedule(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="schedules")  # Link to the User model
    start_time = models.DateTimeField()  # Start date and time of the irrigation
    end_time = models.DateTimeField()    # End date and time of the irrigation

    def __str__(self):
        return f"Schedule from {self.start_time} to {self.end_time}"

    def get_plans(self):
        """Return all plans associated with this schedule."""
        return self.plans.all()
    
class IrrigationPlan(models.Model):
    id = models.AutoField(primary_key=True)
    schedule = models.ForeignKey(IrrigationSchedule, on_delete=models.CASCADE, related_name="plans", null=True)  # Make foreign key nullable
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    date_heure = models.DateTimeField() 
    quantite_eau = models.FloatField()   
    zone = models.CharField(max_length=255)  

    def __str__(self):
        return f"Irrigation Plan: {self.zone} at {self.date_heure}"
