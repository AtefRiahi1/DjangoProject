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

    recommandation = models.ForeignKey(Recommandation, on_delete=models.CASCADE)  # Lier le feedback à une recommandation
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Lier le feedback à un utilisateur
    feedback_type = models.CharField(max_length=10, choices=FEEDBACK_CHOICES, default=LIKE)
    created_at = models.DateTimeField(auto_now_add=True)  # Date de création du feedback

    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"
        unique_together = ('recommandation', 'user')  # Un utilisateur peut "liker" ou "disliker" une recommandation une seule fois

    def __str__(self):
        return f"{self.user.username} a {self.get_feedback_type_display()} la recommandation '{self.recommandation.conseil}'"
