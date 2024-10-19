from django.db import models
from accounts.models import User
from django.conf import settings

class ZoneIrrigation(models.Model):
    nom_zone = models.CharField(max_length=100)
    superficie = models.FloatField()
    type_sol = models.CharField(max_length=100)
    besoin_eau = models.FloatField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)  # Rendre le champ nullable
    image_zone = models.ImageField(upload_to='images_zones/', null=True, blank=True) 

    def __str__(self):
        return self.nom_zone