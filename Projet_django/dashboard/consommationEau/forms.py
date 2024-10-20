from django import forms 
from consommationEau.models import *

# Service Page SEO Form
class consommationEauPageSEOForm(forms.ModelForm):
    class Meta:
        model = consommationEauPageSEO
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'