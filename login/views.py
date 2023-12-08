from django.contrib.auth.views import LoginView
from .forms import CustomAuthForm
from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404

from eventapp.models import logourl, events_details

from django.contrib.auth import views as auth_views

from datetime import date, datetime

from django.utils import timezone

from django.db.models import Q


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add your custom context here
        context['logourl'] = logourl.objects.all()
        return context

def logindash(request):
    now = timezone.now()
    upcoming_events = events_details.objects.filter(Q(events_schedule__gte=now)&Q(apr = 1))

    context = {
        'now': now,
        'upcoming_events': upcoming_events,
    }

    return render(request, 'login/logindash.html', context)



class CustomLogoutView(auth_views.LogoutView):
    template_name = 'login/logout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add your custom context here
        context['logourl'] = logourl.objects.all()
        return context
