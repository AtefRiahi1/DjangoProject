from django.db import models

class Capteur(models.Model):
    TYPE_CHOICES = [
        ('temperature', 'Temperature Sensor'),
        ('humidity', 'Humidity Sensor'),
    ]
    nom_capteur = models.CharField(max_length=100,default='nom_capteur')
    type_capteur = models.CharField(max_length=50, choices=TYPE_CHOICES)
    localisation = models.CharField(max_length=100)
    status = models.BooleanField(default=True)  # True = actif, False = inactif
    image_capteur = models.ImageField(upload_to='images_capteurs/', null=True, blank=True)
    date_installation = models.DateField()

    def __str__(self):
        return f"{self.type_capteur} - {self.localisation}"
