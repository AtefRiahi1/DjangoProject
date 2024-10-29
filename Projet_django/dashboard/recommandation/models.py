from django.conf import settings
from django.db import models
from accounts.models import User

class Recommandation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # Rendre le champ nullable
    conseil = models.TextField()
    date_recommandation = models.DateField()

    # Nouveaux attributs ajoutés
    crop_type = models.CharField(max_length=100, default='Inconnu')  # Valeur par défaut
    region = models.CharField(max_length=100, default='Sousse')  # Région
    average_temperature = models.FloatField(null=True)  # Rendre nullable
    total_precipitation = models.FloatField(default=20)  # Précipitation totale

    class Meta:
        verbose_name = "Recommandation"
        verbose_name_plural = "Recommandations"

    def __str__(self):
        return f"Recommandation : {self.conseil} - {self.date_recommandation}"

class Feedback(models.Model):
    LIKE = 'like'
    DISLIKE = 'dislike'
    FEEDBACK_CHOICES = [
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike'),
    ]

    recommandation = models.ForeignKey(Recommandation, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback_type = models.CharField(max_length=10, choices=FEEDBACK_CHOICES, null=True, blank=True)  # Rendre nullable
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"

    def __str__(self):
        return f"{self.user.username} a {self.get_feedback_type_display() if self.feedback_type else 'laissé un commentaire'} sur la recommandation '{self.recommandation.conseil}'"
