from time import strptime
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw

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
    apr = models.IntegerField(blank=True, null=True, default=0)

    # Modify the ips_url field to use choices
    IPS_URL_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
    ]
    
    ips_online = models.CharField(max_length=7, choices=IPS_URL_CHOICES, default='offline')

    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    CERTIFICATE_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]

    cert_allowed = models.CharField(max_length=3, choices=CERTIFICATE_CHOICES, default='Yes')

    history = HistoricalRecords()

    def __str__(self):
    	return str(self.events_name)+" "+" "+str(self.events_requestor)+" "+str(self.events_details_id)

    def save(self, *args, **kwargs):
    	url = "https://evmfeucavite.pythonanywhere.com/eventapp/deta/" + str(self.events_details_id)
    	qrcode_img = qrcode.make(url)
    	canvas = Image.new('RGB', (400, 400), 'white')
    	draw = ImageDraw.Draw(canvas)
    	canvas.paste(qrcode_img)
    	fname = f'qr_code-{self.events_name}.png'
    	buffer = BytesIO()
    	canvas.save(buffer,'PNG')
    	self.qr_code.save(fname, File(buffer), save = False)
    	canvas.close()
    	super().save(*args, **kwargs)

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

class AttendanceMonitoring2(models.Model):
	attendee = models.CharField(max_length=255, blank=True, null=True)
	events_details_id = models.CharField(max_length=255, blank=True, null=True)
	sess_id = models.CharField(max_length=255, blank=True, null=True)
	time_in = models.DateTimeField(auto_now_add=True, blank=True, null=True)

	history = HistoricalRecords()

	def __str__(self):
		return self.events_details_id+" "+str(self.attendee)+" "+str(self.sess_id)

class AttendanceMonitoring3(models.Model):
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

class ecert(models.Model):
    event_id = models.CharField(max_length=255, blank=True, null=True)
    attendee = models.CharField(max_length=255, blank=True, null=True)
    q1 = models.IntegerField(null = True, blank = True, default = 1)
    q2 = models.IntegerField(null = True, blank = True, default = 1)
    q3 = models.IntegerField(null = True, blank = True, default = 1)
    q4 = models.IntegerField(null = True, blank = True, default = 1)
    avg = models.FloatField(blank=True, null=True)
    feedback = models.CharField(max_length=255, blank=True, null=True)
    date_performed = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.event_id+" "+str(self.attendee)+" "+str(self.date_performed)

class ipsurl(models.Model):
	ipsurl = models.CharField(max_length=255, blank=True, null=True)

	def __str__(self):
		return str(self.ipsurl)

class logourl(models.Model):
	logourl = models.CharField(max_length=255, blank=True, null=True)

	def __str__(self):
		return str(self.logourl)

class qform(models.Model):
	event_id = models.CharField(max_length=255, blank=True, null=True)
	question = models.CharField(max_length=255, blank=True, null=True)
	category = models.CharField(max_length=255, blank=True, null=True)
	q_number = models.IntegerField(null = True, blank = True, default = 1)

	def __str__(self):
		return str(self.event_id)+" "+str(self.category)