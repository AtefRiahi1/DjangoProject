from django.db import models

class Capteur(models.Model):
    TYPE_CHOICES = [
        ('temperature', 'Temperature Sensor'),
        ('humidity', 'Humidity Sensor'),
    ]
    nom_capteur = models.CharField(max_length=100,default='nom_capteur')
    type_capteur = models.CharField(max_length=50, choices=TYPE_CHOICES,default='humidity')
    localisation = models.CharField(max_length=100,default='Tunisie')
    status = models.BooleanField(default=True)  # True = actif, False = inactif
    image_capteur = models.ImageField(upload_to='images_capteurs/', null=True, blank=True)
    date_installation = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_type_capteur_display()} - {self.localisation}"

class Mesure(models.Model):
    capteur = models.ForeignKey(Capteur, on_delete=models.CASCADE, related_name='mesures')
    temperature = models.FloatField()
    moisture = models.FloatField()
    should_irrigate = models.BooleanField(default=False)  # Store prediction result
    date_mesure = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mesure du {self.date_mesure} - Capteur: {self.capteur.nom_capteur}"