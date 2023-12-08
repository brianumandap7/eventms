from django.urls import path
from django.urls.resolvers import URLPattern
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views
from login import views as user_views
from .forms import CustomAuthForm
from .views import CustomLoginView, CustomLogoutView

app_name = 'login'

urlpatterns = [
     path('login/', CustomLoginView.as_view(), name='login-login'),
     path('logout/', CustomLogoutView.as_view(), name='login-logout'),

     path('', views.logindash, name='logindash'),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
