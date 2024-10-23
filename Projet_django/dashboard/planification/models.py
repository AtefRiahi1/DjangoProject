from django.db import models
from accounts.models import User
# Create your models here.
class IrrigationPlan(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    date_heure = models.DateTimeField() 
    quantite_eau = models.FloatField()   
    zone = models.CharField(max_length=255)  

    def __str__(self):
        return f"Irrigation Plan: {self.zone} at {self.date_heure}"