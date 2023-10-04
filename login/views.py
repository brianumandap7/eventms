from django.contrib.auth.views import LoginView
from .forms import CustomAuthForm

class CustomLoginView(LoginView):
    template_name = 'login/login.html'
    authentication_form = CustomAuthForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        # Authentication was successful.
        # You can customize messages or actions here for successful login.
        self.request.session['welcome_message'] = 'Welcome, {}'.format(form.cleaned_data['username'])
        return super().form_valid(form)

    def form_invalid(self, form):
        # Authentication failed.
        # You can add custom error messages here, e.g., for inactive users.
        if form.errors.get('__all__'):
            if 'non_existent_user' in form.errors['__all__'][0]:
                # Handle non-existent user error
                form.add_error(None, form.error_messages['non_existent_user'])

        return super().form_invalid(form)
