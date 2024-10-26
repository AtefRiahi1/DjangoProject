from django import forms
from .models import IrrigationPlan

class IrrigationPlanForm(forms.ModelForm):
    class Meta:
        model = IrrigationPlan  
        fields = ['date_heure', 'quantite_eau', 'zone']  

class LocationForm(forms.Form):
    location = forms.CharField(label='Location', max_length=100, required=True)        