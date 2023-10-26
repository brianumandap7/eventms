from time import strptime
from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime
from django.utils import timezone

from simple_history.models import HistoricalRecords


class events_details(models.Model):
    events_details_id = models.AutoField(primary_key=True)
    events_name = models.CharField(max_length=250, blank=True, null=True)
    events_details = models.CharField(max_length=250, blank=True, null=True)
    events_schedule = models.DateTimeField()
    events_requestor = models.ForeignKey(User, on_delete=models.CASCADE)


    ips_url = models.CharField(max_length=250, blank=True, null=True)
    event_active = models.IntegerField(blank=True, null=True, default=1)
    added_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    # Modify the ips_url field to use choices
    IPS_URL_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
    ]
    
    ips_online = models.CharField(max_length=7, choices=IPS_URL_CHOICES, default='offline')

    history = HistoricalRecords()

    def __str__(self):
    	return str(self.events_name)+" "+" "+str(self.events_requestor)

class UserProfile(models.Model):
    COURSE_CHOICES = [
		('BSIT', 'BSIT'),
		('BSBA', 'BSBA'),
		('BSHRM', 'BSHRM'),
		('BSTM', 'BSTM',),
		('BSeD', 'BSeD'),
		('BSPSYC', 'BSPSYC'),
		('BSPS', 'BSPS'),
		('BSMT', 'BSMT')
    ]
    ROLE_CHOICES = [
    	('Student', 'Student'),
    	('Teacher', 'Teacher'),
    	('Guest', 'Guest'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=255, blank=True, choices=ROLE_CHOICES, null=True)
    course = models.CharField(max_length=255, blank=True, choices=COURSE_CHOICES, null=True)
    new_pass = models.CharField(max_length=255, blank=True, default = "0", null=True)

    history = HistoricalRecords()

    def __str__(self):
        return self.user.username

class AttendanceMonitoring(models.Model):
	attendee = models.CharField(max_length=255, blank=True, null=True)
	events_details_id = models.CharField(max_length=255, blank=True, null=True)
	sess_id = models.CharField(max_length=255, blank=True, null=True)
	time_in = models.DateTimeField(auto_now_add=True, blank=True, null=True)

	history = HistoricalRecords()

	def __str__(self):
		return self.events_details_id+" "+str(self.attendee)+" "+str(self.sess_id)

class UserLogs(models.Model):
    user = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    performed_by = models.CharField(max_length=255, blank=True, null=True)
    date_performed = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    history = HistoricalRecords()

    def __str__(self):
        return self.user+" "+str(self.description)+" "+str(self.date_performed)

class EventLogs(models.Model):
    event_id = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    performed_by = models.CharField(max_length=255, blank=True, null=True)
    date_performed = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    history = HistoricalRecords()

    def __str__(self):
        return self.event_id+" "+str(self.description)+" "+str(self.date_performed)

class EventParticipants(models.Model):
	event = models.ForeignKey(events_details, on_delete=models.SET_NULL, blank=True, null=True, related_name='event_participant')
	ei = models.CharField(max_length=255, blank=True, null=True)
	attendee = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, blank=True, null=True, related_name='attendee')

	def __str__(self):
		return str(self.event)+" "+str(self.attendee)