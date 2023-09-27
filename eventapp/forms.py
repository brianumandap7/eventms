from django import forms
from .models import events_details  # Import your model

class EventsDetailsForm(forms.ModelForm):
    
    class Meta:
        model = events_details
        fields = ['events_name', 'events_details', 'events_schedule', 'ips_url']
        widgets = {
            'events_name': forms.TextInput(attrs={'class': 'form-control'}),
            'events_details': forms.TextInput(attrs={'class': 'form-control'}),
            'ips_url': forms.TextInput(attrs={'class': 'form-control'}),
            'events_schedule': forms.DateTimeInput(attrs={'class':'form-control datetime-input'}),
        }

    def __init__(self, user, *args, **kwargs):
        super(EventsDetailsForm, self).__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        instance = super(EventsDetailsForm, self).save(commit=False)
        instance.events_requestor = self.user
        if commit:
            instance.save()
        return instance
