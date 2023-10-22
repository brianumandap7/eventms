from django.db.models import Q
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomAuthForm(AuthenticationForm):
    error_messages = {
        'invalid_login': 'Failed to log in. Please check your credentials.',
        'inactive': 'Your account is deactivated. Please contact your system administrator.',
    }

    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username or Email'}),
        label=False,
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control pword', 'placeholder': 'Password'}),
        label=False,  # Remove the label for the password field
    )
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            if '@' in username:
                # If the username contains '@', assume it's an email address
                user = User.objects.filter(email=username).first()
            else:
                user = User.objects.filter(username=username).first()

            if user is not None and user.check_password(password):
                if user.is_active:
                    self.user_cache = user
                else:
                    raise forms.ValidationError(
                        self.error_messages['inactive'],
                        code='inactive',
                    )
            else:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                )

        return self.cleaned_data
