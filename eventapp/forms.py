from django import forms
from .models import events_details
from django.contrib.auth.models import User  # Import your model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UserProfile, EventParticipants, qform

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

class EventsDetailsEditForm(forms.ModelForm):
    
    class Meta:
        model = events_details
        fields = ['events_name', 'events_details', 'events_schedule', 'ips_online']
        widgets = {
            'events_name': forms.TextInput(attrs={'class': 'form-control'}),
            'events_details': forms.TextInput(attrs={'class': 'form-control'}),
            'ips_online': forms.Select(attrs={'class': 'form-control'}),
            'events_schedule': forms.DateTimeInput(attrs={'class': 'form-control datetime-input'}),
        }

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        
        # Add Bootstrap classes to form fields
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        

class CustomUserEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(CustomUserEditForm, self).__init__(*args, **kwargs)
        
        # Add Bootstrap classes to form fields
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'

        # Remove password fields from the form
        self.fields.pop('password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['course', 'role']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)

        self.fields['course'].widget.attrs['class'] = 'form-control'
        self.fields['role'].widget.attrs['class'] = 'form-control'

class EventParticipantForm(forms.ModelForm):
    class Meta:
        model = EventParticipants
        fields = ['event', 'attendee']

    def __init__(self, *args, **kwargs):
        event = kwargs.pop('event', None)
        super(EventParticipantForm, self).__init__(*args, **kwargs)

        # Hide the 'event' field and set its initial value
        self.fields['event'].widget = forms.HiddenInput()
        self.fields['event'].label = False
        self.fields['event'].initial = event

        # Customize the queryset for the 'attendee' field to exclude existing participants
        if event:
            existing_participants = EventParticipants.objects.filter(event=event)
            existing_attendees = existing_participants.values_list('attendee_id', flat=True)
            self.fields['attendee'].queryset = UserProfile.objects.exclude(id__in=existing_attendees)

        # Add a CSS class to the 'attendee' field
        self.fields['attendee'].widget.attrs['class'] = 'form-control'

class DateRangeForm(forms.Form):
    start_date = forms.DateTimeField(label='Start Date', widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control sd'}))
    end_date = forms.DateTimeField(label='End Date', widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control sd'}))

class QForm(forms.ModelForm):
    class Meta:
        model = qform
        exclude = ['event_id']

        widgets = {
            'question': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),  # You can adjust the 'rows' attribute as needed
            'category': forms.TextInput(attrs={'class': 'form-control'}),
        }