from django.urls import path
from django.urls.resolvers import URLPattern
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = 'ticket'

urlpatterns = [
    path('admindash/', views.admindash, name='admindash'),
    path('stu/', views.stu, name='stu'),
    path('sao/', views.sao, name='sao'),
    path('create_event/', views.create_event, name='create_event'),

    path('view_event/', views.view_event, name='view_event'),

    path('edit_event/<int:event_id>', views.edit_event, name='edit_event'),

    path('ar/<int:tag>', views.ar, name='ar'),

    path('ua/<int:tag>', views.ua, name='ua'),

    path('manage_users/', views.manage_users, name='manage_users'),

    path('create_user/', views.create_user, name='create_user'),

    path('edit_profile/<int:pk>/', views.edit_profile, name='edit_profile'),

    path('activate/<int:tag>/<str:un>', views.activate, name='activate'),

    path('deact/<int:tag>/<str:un>', views.deact, name='deact'),

    path('ips/<str:sid>/<str:u1>.<str:u2>', views.ips, name='ips'),
    
    path('attendance/', views.attendance, name='attendance'),

    path('radar/', views.radar, name='radar'),

    path('user_logs/<int:tag>/<str:un>', views.user_logs, name='user_logs'),

    path('simple_upload/', views.SimpleUpload, name='simple_upload'),

    path('set_default_password/<int:user_id>/<str:deta>', views.set_default_password, name='set_default_password'),

    path('hist/<int:tag>/<str:un>', views.hist, name='hist'),

    path('super_user_logs/<int:tag>/<str:un>', views.super_user_logs, name='super_user_logs'),

]

urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)


