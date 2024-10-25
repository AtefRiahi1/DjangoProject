from django import forms
from .models import Feedback, Recommandation

# Définition des choix de régions en dehors de la classe
REGION_CHOICES = [
    ("Tunis", "Tunis"),
    ("Ariana", "Ariana"),
    ("Ben Arous", "Ben Arous"),
    ("Manouba", "Manouba"),
    ("Nabeul", "Nabeul"),
    ("Zaghouan", "Zaghouan"),
    ("Bizerte", "Bizerte"),
    ("Béja", "Béja"),
    ("Jendouba", "Jendouba"),
    ("Le Kef", "Le Kef"),
    ("Siliana", "Siliana"),
    ("Sousse", "Sousse"),
    ("Monastir", "Monastir"),
    ("Mahdia", "Mahdia"),
    ("Kairouan", "Kairouan"),
    ("Kasserine", "Kasserine"),
    ("Sidi Bouzid", "Sidi Bouzid"),
    ("Gabès", "Gabès"),
    ("Médenine", "Médenine"),
    ("Tataouine", "Tataouine"),
    ("Gafsa", "Gafsa"),
    ("Tozeur", "Tozeur"),
    ("Kebili", "Kebili"),
    ("Sfax", "Sfax"),
]

class RecommandationForm(forms.ModelForm):
    class Meta:
        model = Recommandation
        fields = ['conseil', 'date_recommandation', 'crop_type', 'region', 'average_temperature', 'total_precipitation']
        widgets = {
            'conseil': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Entrez le conseil'}),
            'date_recommandation': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'crop_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type de culture'}),
            'region': forms.Select(choices=REGION_CHOICES, attrs={'class': 'form-select'}),  # Utilisation de REGION_CHOICES ici
            'average_temperature': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Température moyenne'}),
            'total_precipitation': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Précipitation totale'}),
        }
class FeedbackForm(forms.ModelForm):
    like = forms.BooleanField(required=False, label="Like")
    dislike = forms.BooleanField(required=False, label="Dislike")

    class Meta:
        model = Feedback
        fields = ['like', 'dislike']  # Incluez d'autres champs comme 'comment' si nécessaire

    def clean(self):
        cleaned_data = super().clean()
        like = cleaned_data.get('like')
        dislike = cleaned_data.get('dislike')

        # Vérifiez que l'utilisateur ne peut pas cocher à la fois 'like' et 'dislike'
        if like and dislike:
            raise forms.ValidationError("Vous ne pouvez pas sélectionner à la fois 'like' et 'dislike'.")
        
        return cleaned_data

