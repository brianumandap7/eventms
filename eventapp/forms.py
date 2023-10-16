from django import forms
from .models import events_details
from django.contrib.auth.models import User  # Import your model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UserProfile

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
        fields = ['events_name', 'events_details', 'events_schedule', 'ips_url']
        widgets = {
            'events_name': forms.TextInput(attrs={'class': 'form-control'}),
            'events_details': forms.TextInput(attrs={'class': 'form-control'}),
            'ips_url': forms.TextInput(attrs={'class': 'form-control'}),
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
