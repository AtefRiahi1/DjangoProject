from django import forms
from .models import Capteur

class CapteurForm(forms.ModelForm):
    class Meta:
        model = Capteur
        fields = ['nom_capteur','type_capteur', 'localisation', 'status','image_capteur', 'date_installation']
        widgets = {
            'nom_capteur': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez le nom du capteur'
            }),
            'type_capteur': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'localisation': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez la localisation'
            }),
            'status': forms.RadioSelect(attrs={
                'class': 'form-control',
            }),
            'image_capteur': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'date_installation': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'}),
        }

