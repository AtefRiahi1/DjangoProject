from django import forms
from .models import IrrigationPlan

class IrrigationPlanForm(forms.ModelForm):
    class Meta:
        model = IrrigationPlan  
        fields = ['date_heure', 'quantite_eau', 'zone']  