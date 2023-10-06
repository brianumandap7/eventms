from time import strptime
from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime
from django.utils import timezone

class events_details(models.Model):
    events_details_id = models.AutoField(primary_key=True)
    events_name = models.CharField(max_length=250, blank=True, null=True)
    events_details = models.CharField(max_length=250, blank=True, null=True)
    events_schedule = models.DateTimeField()
    events_requestor = models.ForeignKey(User, on_delete=models.CASCADE)
    ips_url = models.CharField(max_length=250, blank=True, null=True)
    event_active = models.IntegerField(blank=True, null=True, default=1)

    def __str__(self):
    	return str(self.events_name)+" "+" "+str(self.events_requestor)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=255, blank=True, null=True)
    course = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username

class AttendanceMonitoring(models.Model):
	attendee = models.CharField(max_length=255, blank=True, null=True)
	events_details_id = models.CharField(max_length=255, blank=True, null=True)
	sess_id = models.CharField(max_length=255, blank=True, null=True)
	time_in = models.DateTimeField(auto_now_add=True, blank=True, null=True)

	def __str__(self):
		return self.events_details_id+" "+str(self.attendee)+" "+str(self.sess_id)