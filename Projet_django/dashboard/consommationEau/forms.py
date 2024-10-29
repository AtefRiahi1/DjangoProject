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

class ConsommationMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.date_heure} - {obj.quantite_consommee} L"

class IrrigationForm(forms.ModelForm):
    consommations = ConsommationMultipleChoiceField(
        queryset=ConsommationEau.objects.none(),  # Par défaut, aucun résultat
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Sélectionnez les consommations"
    )

    def __init__(self, *args, user=None, **kwargs):  # Ajoutez user ici
        self.user = user  # Stockez l'utilisateur dans l'instance du formulaire
        super().__init__(*args, **kwargs)
        # Filtrer les consommations pour l'utilisateur connecté
        self.fields['consommations'].queryset = ConsommationEau.objects.filter(user=user)
        if self.instance and self.instance.pk:
            self.fields['consommations'].initial = self.instance.get_consommations()

    class Meta:
        model = Irrigation
        fields = ['nom', 'type_irrigation', 'description', 'consommations']

    def save(self, commit=True):
        irrigation = super().save(commit=False)  # Crée ou met à jour l'objet Irrigation sans le sauvegarder
        
        # Associer l'irrigation à l'utilisateur connecté
        irrigation.user = self.user  # Assurez-vous que l'utilisateur est bien assigné

        if commit:
            irrigation.save()  # Enregistre l'objet Irrigation d'abord

            # Associer les consommations sélectionnées à l'irrigation
            if self.cleaned_data['consommations']:
                for consommation in self.cleaned_data['consommations']:
                    consommation.irrigation = irrigation  # Affectation de l'irrigation
                    consommation.save()  # Sauvegarde de la consommation avec la nouvelle irrigation

        return irrigation  # Retourne l'objet Irrigation
