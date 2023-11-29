from django.urls import path
from django.urls.resolvers import URLPattern
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib.admin.views.decorators import staff_member_required

from django.contrib.auth.decorators import login_required

app_name = 'ticket'

urlpatterns = [
    path('admindash/', login_required(views.admindash), name='admindash'),
    path('stu/', login_required(views.stu), name='stu'),
    path('sao/', login_required(views.sao), name='sao'),
    path('create_event/', staff_member_required(views.create_event), name='create_event'),

    path('view_event/', staff_member_required(views.view_event), name='view_event'),

    path('edit_event/<int:event_id>', staff_member_required(views.edit_event), name='edit_event'),

    path('ar/<int:tag>', staff_member_required(views.ar), name='ar'),

    path('ua/<int:tag>', staff_member_required(views.ua), name='ua'),

    path('manage_users/', staff_member_required(views.manage_users), name='manage_users'),

    path('create_user/', staff_member_required(views.create_user), name='create_user'),

    path('edit_profile/<int:pk>/', staff_member_required(views.edit_profile), name='edit_profile'),

    path('activate/<int:tag>/<str:un>', staff_member_required(views.activate), name='activate'),

    path('deact/<int:tag>/<str:un>', staff_member_required(views.deact), name='deact'),

    path('ips/<str:sid>/<str:u1>.<str:u2>/<str:tag>', views.ips, name='ips'),

    path('ips2/<str:sid>/<str:u1>.<str:u2>/<str:tag>', views.ips2, name='ips2'),

    path('ips3/<str:sid>/<str:u1>.<str:u2>/<str:tag>', views.ips3, name='ips3'),
    
    path('attendance/<int:tag>', views.attendance, name='attendance'),

    path('attendance2/<int:tag>', views.attendance2, name='attendance2'),

    path('attendance3/<int:tag>', views.attendance3, name='attendance3'),

    path('radar/<int:tag>', views.radar, name='radar'),

    path('cw/', views.cw, name='cw'),

    path('user_logs/<int:tag>/<str:un>', staff_member_required(views.user_logs), name='user_logs'),

    path('simple_upload/', staff_member_required(views.SimpleUpload), name='simple_upload'),

    path('set_default_password/<int:user_id>/<str:deta>', staff_member_required(views.set_default_password), name='set_default_password'),

    path('hist/<int:tag>/<str:un>', staff_member_required(views.hist), name='hist'),

    path('super_user_logs/<int:tag>/<str:un>', staff_member_required(views.super_user_logs), name='super_user_logs'),

    path('super_user_elogs/<int:tag>/<str:un>', staff_member_required(views.super_user_elogs), name='super_user_elogs'),

    path('calendar/', staff_member_required(views.calendar), name='calendar'),

    path('view_user/<int:tag>', staff_member_required(views.view_user), name='view_user'),

    path('event_det/<int:tag>', staff_member_required(views.event_det), name='event_det'),

    path('filter_user/', staff_member_required(views.filter_user), name='filter_user'),
    path('filter_event/', staff_member_required(views.filter_event), name='filter_event'),

    path('p_reset/', views.p_reset, name='p_reset'),

    path('change_p/', views.change_p, name='change_p'),

    path('rpo/<str:un>', views.rpo, name='rpo'),

    path('radar_dash/', views.radar_dash, name='radar_dash'),

    path('ecerts/', login_required(views.ecerts), name='ecerts'),

    path('ecerts1/<int:tag>', login_required(views.ecerts1), name='ecerts1'),

    path('approve_event/', staff_member_required(views.approve_event), name='approve_event'),

    path('apr/<int:tag>', staff_member_required(views.apr), name='apr'),

    path('fform/<int:tag>', login_required(views.fform), name='fform'),

    path('q_form/<int:tag>', login_required(views.q_form), name='q_form'),

    path('ana/<int:tag>', login_required(views.ana), name='ana'),

    path('removeq/<int:tag>/<int:ref>', login_required(views.removeq), name='removeq'),

    path('deta/<int:tag>', login_required(views.deta), name='deta'),

    path('remp/<int:tag>/<int:tag2>', login_required(views.remp), name='remp'),

]

urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)


