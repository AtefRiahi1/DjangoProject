from django import forms
from .models import IrrigationPlan, IrrigationSchedule

class IrrigationPlanForm(forms.ModelForm):
    class Meta:
        model = IrrigationPlan  
        fields = ['date_heure', 'quantite_eau', 'zone']  

class LocationForm(forms.Form):
    location = forms.CharField(label='Location', max_length=100, required=True)        

class IrrigationScheduleForm(forms.ModelForm):
    irrigation_plans = forms.ModelMultipleChoiceField(
        queryset=IrrigationPlan.objects.none(), 
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = IrrigationSchedule
        fields = ['start_time', 'end_time']

    def __init__(self, *args, **kwargs):
        # Allow passing in the irrigation schedule instance
        schedule_instance = kwargs.pop('schedule_instance', None)
        super().__init__(*args, **kwargs)
        if schedule_instance:
            self.fields['irrigation_plans'].queryset = IrrigationPlan.objects.filter(user=schedule_instance.user)
            self.fields['irrigation_plans'].initial = schedule_instance.plans.all()