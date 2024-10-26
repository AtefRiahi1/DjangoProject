from django import forms
from .models import Capteur, Mesure

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
                'class': 'form-select',
            }),
            'localisation': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez la localisation'
            }),
            'status': forms.CheckboxInput(attrs={
                'class': 'form-check',
            }),
            'image_capteur': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'date_installation': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'}),
        }

class MesureForm(forms.ModelForm):
    class Meta:
        model = Mesure
        fields = ['temperature', 'humidity']
        widgets = {
            'temperature': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez la temperature'
            }),
            'humidity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez la humidité'
            }),
        }