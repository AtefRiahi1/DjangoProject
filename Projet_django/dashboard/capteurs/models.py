from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator

class Capteur(models.Model):
    TYPE_CHOICES = [
        ('temperature', 'Temperature Sensor'),
        ('humidity', 'Humidity Sensor'),
    ]

    # Add validators
    nom_capteur = models.CharField(
        max_length=100,
        default='nom_capteur',
        validators=[RegexValidator(r'^[a-zA-Z\s]*$', 'Seulement des letters et des espaces sont autorisés')]
    )
    type_capteur = models.CharField(max_length=50, choices=TYPE_CHOICES, default='humidity')
    localisation = models.CharField(
        max_length=100,
        default='Tunisie',
        validators=[RegexValidator(r'^[a-zA-Z\s]*$', 'Seulement des letters et des espaces sont autorisés')]
    )
    status = models.BooleanField(default=True)  # True = actif, False = inactif
    image_capteur = models.ImageField(upload_to='images_capteurs/', null=True, blank=True)
    date_installation = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_type_capteur_display()} - {self.localisation}"

class Mesure(models.Model):
    capteur = models.ForeignKey(Capteur, on_delete=models.CASCADE, related_name='mesures')
    # Add validators for temperature and moisture
    temperature = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
    )
    moisture = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(10000.0)]
    )
    should_irrigate = models.BooleanField(default=False)  # Store prediction result
    date_mesure = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mesure du {self.date_mesure} - Capteur: {self.capteur.nom_capteur}"