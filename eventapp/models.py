from time import strptime
from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime

class events_details(models.Model):
    events_details_id = models.AutoField(primary_key=True)
    events_name = models.CharField(max_length=250, blank=True, null=True)
    events_details = models.CharField(max_length=250, blank=True, null=True)
    events_schedule = models.DateTimeField()
    events_requestor = models.ForeignKey(User, on_delete=models.CASCADE)

    ips_url = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
    	return str(self.events_name)+" "+" "+str(self.events_requestor)