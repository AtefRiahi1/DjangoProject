from django import forms
from .models import ZoneIrrigation ,MaintenanceSchedule

class ZoneIrrigationForm(forms.ModelForm):
    class Meta:
        model = ZoneIrrigation
        fields = ['nom_zone', 'superficie', 'type_sol', 'image_zone']  
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

 


class MaintenanceScheduleForm(forms.ModelForm):
    class Meta:
        model = MaintenanceSchedule
        fields = ['date_maintenance', 'description', 'completed', 'zone_irrigation']
        widgets = {
            'date_maintenance': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'placeholder': 'Date de maintenance'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Description de la maintenance',
                'rows': 3,
            }),
            'completed': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'zone_irrigation': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

    def clean_date_maintenance(self):
        date_maintenance = self.cleaned_data.get('date_maintenance')
        if date_maintenance is None:
            raise forms.ValidationError("La date de maintenance est requise.")
        return date_maintenance

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if not description:
            raise forms.ValidationError("La description est requise.")
        return description
