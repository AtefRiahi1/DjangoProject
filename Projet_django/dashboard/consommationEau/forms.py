from django import forms 
from consommationEau.models import *
from home.models import *

# Service Page SEO Form
class consommationEauPageSEOForm(forms.ModelForm):
    class Meta:
        model = consommationEauPageSEO
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class ConsommationEauFormF(forms.ModelForm):
    class Meta:
        model = ConsommationEau
        fields = '__all__'
        exclude = ['user'] 
        widgets = {
            'date_heure': forms.DateTimeInput(attrs={
                'class': 'form-control', 
                'type': 'datetime-local'  # Utilise le type HTML5 pour le champ datetime
            }),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'  