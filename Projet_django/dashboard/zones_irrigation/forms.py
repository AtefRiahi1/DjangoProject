from django import forms
from .models import ZoneIrrigation

class ZoneIrrigationForm(forms.ModelForm):
    class Meta:
        model = ZoneIrrigation
        fields = ['nom_zone', 'superficie', 'type_sol', 'besoin_eau', 'image_zone']  
        widgets = {
            'nom_zone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez le nom de la zone'
            }),
            'superficie': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez la superficie en ha'
            }),
            'type_sol': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'besoin_eau': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez le besoin en eau en m³'
            }),
            'image_zone': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),  # Widget pour le champ de fichier
        }

    def clean_superficie(self):
        superficie = self.cleaned_data.get('superficie')
        if superficie <= 0:
            raise forms.ValidationError("La superficie doit être un nombre positif.")
        return superficie

    def clean_besoin_eau(self):
        besoin_eau = self.cleaned_data.get('besoin_eau')
        if besoin_eau <= 0:
            raise forms.ValidationError("Le besoin en eau doit être un nombre positif.")
        return besoin_eau
