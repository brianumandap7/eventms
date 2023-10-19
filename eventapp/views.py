from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.contrib.auth.models import User
from .forms import EventsDetailsForm, EventsDetailsEditForm, CustomUserCreationForm, CustomUserEditForm, UserProfileForm, EventParticipantForm
from .models import events_details, UserProfile, AttendanceMonitoring, UserLogs, HistoricalUserLogs, HistoricalEventLogs, EventLogs, EventParticipants
from django.contrib import messages
from django.views.generic.base import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from tablib import Dataset

from .resources import PersonResource

from django.urls import reverse_lazy, reverse
from .resources import PersonResource
from tablib import Dataset
# Create your views here.
import openpyxl

from django.contrib.auth import get_user_model

from django.contrib.admin.models import LogEntry

from simple_history.models import HistoricalRecords

from django.utils import timezone

from django.http import JsonResponse

from django.db.models import Q

from datetime import date, datetime


from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView
def admindash(request):
	query = {
		's_count': User.objects.all().exclude(is_staff = True).count(),
		't_count': User.objects.all().exclude(is_staff = False).count(),
		'e_count': events_details.objects.all().count(),
	}

	if request.method == 'POST':
		db = User.objects.get(username = request.user)
		new_password = request.POST.get('new_password')
		db.set_password(new_password)
		db.save()

		try:
			user_profile = UserProfile.objects.get(user=request.user)
			user_profile.new_pass = '1'
			user_profile.save()
		except UserProfile.DoesNotExist:
			pass

		messages.success(request, 'Your password was successfully updated.')
		return redirect('/')
	return render(request, 'eventapp/admindash.html', query)

def stu(request):
	session_id = request.session.session_key
	now = timezone.now()
	upcoming_events = events_details.objects.filter(events_schedule__gte=now)
	evt = events_details.objects.filter(events_schedule =now)
	pst = events_details.objects.filter(events_schedule__lt=now)

	for event in upcoming_events:
		print(event.events_schedule, event.event_active)
	query = {
		'session_id': session_id,
		'now': now,
    	'upcoming_events': upcoming_events,
    	'evt': evt,
    	'pst': pst,
    	'up': UserProfile.objects.filter(user = request.user),
	}
	return render(request, 'eventapp/stu.html', query)

def sao(request):
	query = {
		
	}
	return render(request, 'eventapp/sao.html', query)

def create_event(request):
    if request.method == 'POST':
        form = EventsDetailsForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            # Optionally, you can redirect to a success page or display a message
            messages.success(request, 'Event created successfully.')
            return redirect('/eventapp/view_event')  # Change 'success_page' to the actual URL name
    else:
        form = EventsDetailsForm(user=request.user)

    context = {
    	'form': form,
    	'ed': events_details.objects.all().order_by('events_name')
    }

    return render(request, 'eventapp/create_event.html', context)

def view_event(request):
    context = {
    	'ed': events_details.objects.all().order_by('events_name')
    }

    return render(request, 'eventapp/view_event.html', context)

def event_det(request, tag):
    event = events_details.objects.get(events_details_id=tag)
    participants = EventParticipants.objects.filter(event=event)

    if request.method == 'POST':
        form = EventParticipantForm(request.POST, event=event)  # Pass the event object to the form
        if form.is_valid():
            # Get the selected attendee and create a participant with the event and attendee
            attendee = form.cleaned_data['attendee']
            participant = EventParticipants(event=event, attendee=attendee)
            participant.save()
            return redirect('/eventapp/event_det/'+str(tag))
    else:
        form = EventParticipantForm(initial={'event': event}, event=event)  # Pass the event object to the form

    context = {
        'tag': tag,
        'event': event,
        'participants': participants,
        'form': form,
        'ev': events_details.objects.filter(events_details_id=tag),
        'ep': EventParticipants.objects.filter(event_id=tag)
    }

    return render(request, 'eventapp/event_det.html', context)


def edit_event(request, event_id):
    event = get_object_or_404(events_details, pk=event_id)

    if request.method == 'POST':
        form = EventsDetailsEditForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            # Optionally, you can redirect to a success page or display a message
            EventLogs.objects.create(event_id = event_id, description='Event Update Successful', performed_by=request.user)
            messages.success(request, 'Event updated successfully.')
            return redirect('/eventapp/view_event')   # Change 'success_page' to the actual URL name
    else:
        form = EventsDetailsEditForm(instance=event)

    return render(request, 'eventapp/edit_event.html', {'form': form, 'event': event})

def ar(request, tag):
    context = {
    	'tag': tag,
    	'exec': events_details.objects.filter(events_details_id = tag).update(event_active = 0),
    	'alog': EventLogs.objects.create(event_id=tag, description='Event Archived', performed_by=request.user),
    }

    return render(request, 'eventapp/ar.html', context)

def ua(request, tag):
    context = {
    	'tag': tag,
    	'exec': events_details.objects.filter(events_details_id = tag).update(event_active = 1),
    	'alog': EventLogs.objects.create(event_id=tag, description='Event Unarchived', performed_by=request.user),
    }

    return render(request, 'eventapp/ua.html', context)

def manage_users(request):
    context = {
    	'all_users': User.objects.all().exclude(is_superuser = True).order_by('first_name'),
    	'hr': HistoricalRecords(),    
    	'superH': LogEntry.objects.all()
    	}

    return render(request, 'eventapp/manage_users.html', context)

def create_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to a success page or do something else (e.g., login the user)
            messages.success(request, 'User created successfully.')
            return redirect('/eventapp/manage_users')  # Replace 'success_page' with your desired URL
    else:
        form = CustomUserCreationForm()

    return render(request, 'eventapp/create_user.html', {'form': form})

def edit_profile(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            # Redirect to a success page or do something else
            UserLogs.objects.create(user=user.username, description='Profile Update Successful', performed_by=request.user)
            messages.success(request, 'User updated successfully.')
            return redirect('/eventapp/manage_users')  # Replace 'success_page' with your desired URL
    else:
        form = CustomUserEditForm(instance=user)

    context = {
        'form': form,
        'pk': pk,
        'det': User.objects.filter(id = pk)
    }

    return render(request, 'eventapp/edit_profile.html', context)

def deact(request, tag, un):
    context = {
    	'tag': tag,
    	'un': un,
    	'exec': User.objects.filter(id = tag).update(is_active = False),
    	'alog': UserLogs.objects.create(user=un, description='User Deactivated', performed_by=request.user),
    }

    return render(request, 'eventapp/deact.html', context)

def activate(request, tag, un):

    context = {
    	'tag': tag,
    	'un': un,
    	'exec': User.objects.filter(id = tag).update(is_active = True),
    	'alog': UserLogs.objects.create(user=un, description='User Reactivated', performed_by=request.user),
    }

    return render(request, 'eventapp/activate.html', context)

def ips(request, sid, u1, u2):

	context = {
	    	'sid': sid,
	    	'u1': u1,
	    	'u2': u2,
	    	'executed_attendance': AttendanceMonitoring.objects.create(attendee=u1+"."+u2,events_details_id=1,sess_id=sid)
    }
	return render(request, 'eventapp/ips.html', context)

def attendance(request):
    context = {
    	'at': AttendanceMonitoring.objects.all(),
    }

    return render(request, 'eventapp/attendance.html', context)

def radar(request):
    context = {
    	'attendee_count': AttendanceMonitoring.objects.all().count(),
    }

    return render(request, 'eventapp/radar.html', context)

def user_logs(request, tag, un):

    superH = LogEntry.objects.filter(object_repr = un)
    context = {
    	'tag': tag,
    	'un': un,
    	'ulogs': UserLogs.objects.filter(user = un),
    	'us': User.objects.filter(id = tag),
    	'superH': superH,
    	'tn': timezone.now(),
    	'hist': HistoricalUserLogs.objects.filter(user = un)
    }

    return render(request, 'eventapp/user_logs.html', context)

def super_user_logs(request, tag, un):

    superH = LogEntry.objects.filter(object_repr = un)
    context = {
    	'tag': tag,
    	'un': un,
    	'superH': superH,
    	'tn': timezone.now(),
    }

    return render(request, 'eventapp/super_user_logs.html', context)

def cw(request):
    context = {
    	
    }
    return render(request, 'eventapp/cw.html', context)

def super_user_elogs(request, tag, un):

    superH = LogEntry.objects.filter(object_repr__contains = un)
    context = {
    	'tag': tag,
    	'un': un,
    	'superH': superH,
    	'tn': timezone.now(),
    }

    return render(request, 'eventapp/super_user_elogs.html', context)

def hist(request, tag, un):
    context = {
    	'tag': tag,
    	'un': un,
    	'ev': events_details.objects.filter(events_details_id = tag),
    	'hist': HistoricalEventLogs.objects.filter(event_id = tag),
    }

    return render(request, 'eventapp/hist.html', context)

def SimpleUpload(request):
    if request.method == 'POST':
        dataset = Dataset()
        new_person = request.FILES['myfile']

        if not new_person.name.endswith('xlsx'):
            messages.info(request, 'Wrong file format. Please upload an Excel file.')
            return render(request, 'eventapp/simple_upload.html')

        imported_data = dataset.load(new_person.read(), format='xlsx')
        for data in imported_data:
            username = data[1]
            if User.objects.filter(username=username).exists():
                # Skip creating the user if the username already exists
                continue

            # Create the user if the username doesn't exist
            user = User(
                username=username,
                email=data[3],
                first_name=data[4],
                last_name=data[5],
                is_staff=data[6]
            )
            user.set_password(data[2])
            user.save()

        messages.success(request, 'Users created successfully via bulk upload!')
        return HttpResponseRedirect('/eventapp/cw/')
    return render(request, 'eventapp/simple_upload.html')

def set_default_password(request, user_id, deta):
    # Get the user by ID
    User = get_user_model()
    user = User.objects.get(pk=user_id)

    # Set the default password
    default_password = 'P@ssw0rd123'
    user.set_password(default_password)
    user.save()

    #save logs
    execu = UserLogs.objects.create(user=deta, description='Reset Password', performed_by=request.user)
    # Redirect back to the user edit page or any other appropriate page
    messages.success(request, 'Password reset successful!')
    return HttpResponseRedirect('/eventapp/manage_users/')

from django.http import JsonResponse

def calendar(request):
    events = events_details.objects.all()
    event_data = []
    for event in events:
        if event.events_schedule:
            event_data.append({
                'title': event.events_name,
                'start': event.events_schedule.isoformat(),
                'end': event.events_schedule.isoformat(),
                'url': f'/eventapp/hist/{event.events_details_id}/{event.events_name.replace(" ", "%20")}',
            })

    context = {
        'event_data': event_data,
    }

    return render(request, 'eventapp/calendar.html', context)


def view_user(request, tag):
    profile_instance, created = UserProfile.objects.get_or_create(user_id=tag)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile_instance)
        if form.is_valid():
            form.save()
            return redirect('/eventapp/view_user/'+str(tag))
    else:
        form = UserProfileForm(instance=profile_instance)

    context = {
        'tag': tag,
        'up': profile_instance,
        'form': form,
        'up1': UserProfile.objects.filter(user_id = tag),
        'up2': User.objects.filter(id = tag),
    }

    return render(request, 'eventapp/view_user.html', context)

def filter_user(request):
    # Check if the start and end months and year have been provided in the request
    start_month = request.GET.get('start_month')
    end_month = request.GET.get('end_month')
    year = request.GET.get('year')

    users_in_month_range = None

    if start_month and end_month and year:
        # Convert the input into integers
        start_month = int(start_month)
        end_month = int(end_month)
        year = int(year)

        # Perform input validation to ensure that the selected month is valid
        if start_month < 1 or start_month > 12 or end_month < 1 or end_month > 12:
            return render(request, 'error_template.html', {'error_message': 'Invalid month selection'})

        # Calculate the start and end datetime objects for the range
        start_date = datetime(year, start_month, 1)
        
        # Calculate the last day of the end month manually
        if end_month == 12:
            last_day_of_end_month = 31
        else:
            last_day_of_end_month = (datetime(year, end_month + 1, 1) - datetime(year, end_month, 1)).days - 1
        
        end_date = datetime(year, end_month, last_day_of_end_month, 23, 59, 59)

        # Create a Q object to filter the User model based on the date_joined field
        month_range_filter = Q(date_joined__range=(start_date, end_date))

        # Query the User model with the filter
        users_in_month_range = User.objects.filter(month_range_filter)

    context = {
        'users_in_month_range': users_in_month_range,
        'start_month': start_month,
        'end_month': end_month,
        'year': year,
    }

    return render(request, 'eventapp/filter_user.html', context)

def filter_event(request):
    context = {
    	
    }
    return render(request, 'eventapp/filter_event.html', context)



