from django.db import models
from accounts.models import User
from django.conf import settings

class ZoneIrrigation(models.Model):
    nom_zone = models.CharField(max_length=100)
    superficie = models.FloatField()
    type_sol = models.CharField(max_length=100)
    besoin_eau = models.FloatField(default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)  # Rendre le champ nullable
    image_zone = models.ImageField(upload_to='images_zones/', null=True, blank=True) 

    def __str__(self):
        return self.nom_zone

class MaintenanceSchedule(models.Model):
    date_maintenance = models.DateField()  
    description = models.TextField()  
    completed = models.BooleanField(default=False)  
    zone_irrigation = models.ForeignKey(ZoneIrrigation, on_delete=models.CASCADE, related_name='maintenance_schedules')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE) 
    def __str__(self):
        return f"Maintenance on {self.date_maintenance} for {self.zone_irrigation.nom_zone}"