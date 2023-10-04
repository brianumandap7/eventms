from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomAuthForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

    error_messages = {
        'invalid_login': 'Failed to Log in. Contact your System Administrator.',
        'inactive': 'Your account is deactivated. Please contact your System administrator.',
        'non_existent_user': 'Failed to Log in. Contact your System Administrator.',
    }

    def __init__(self, *args, **kwargs):
        super(CustomAuthForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
        self.fields['username'].label = False
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control pword', 'placeholder': 'Password'})
        self.fields['password'].label = False

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = None

            if user is not None and not user.is_active:
                raise forms.ValidationError(
                    self.error_messages['inactive'],
                    code='inactive',
                )
            elif user is None:
                raise forms.ValidationError(
                    self.error_messages['non_existent_user'],
                    code='non_existent_user',
                )

        return super(CustomAuthForm, self).clean()
