from django.db import models
from accounts.models import User


class IrrigationSchedule(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="schedules")  
    start_time = models.DateTimeField()  
    end_time = models.DateTimeField()    

    def __str__(self):
        return f"Schedule from {self.start_time} to {self.end_time}"

    def get_plans(self):
        return self.plans.all()
    
class IrrigationPlan(models.Model):
    id = models.AutoField(primary_key=True)
    schedule = models.ForeignKey(IrrigationSchedule, on_delete=models.CASCADE, related_name="plans", null=True) 
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    date_heure = models.DateTimeField() 
    quantite_eau = models.FloatField()   
    zone = models.CharField(max_length=255)  

    def __str__(self):
        return f"Irrigation Plan: {self.zone} at {self.date_heure}"
