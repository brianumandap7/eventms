from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.contrib.auth.models import User
from .forms import EventsDetailsForm, EventsDetailsEditForm, CustomUserCreationForm, CustomUserEditForm, UserProfileForm, EventParticipantForm, DateRangeForm, QForm
from .models import events_details, UserProfile, AttendanceMonitoring, UserLogs, HistoricalUserLogs, HistoricalEventLogs, EventLogs, EventParticipants, ecert, ipsurl, qform
from django.contrib import messages
from django.views.generic.base import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from tablib import Dataset
from django.db.models import Avg

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

from event.settings import EMAIL_HOST_USER
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView

from django.db.models import F, Max
def admindash(request):
	now = timezone.now()
	upcoming_events = events_details.objects.filter(Q(events_schedule__gte=now)&Q(apr = 1)).count()
	active_users_count = User.objects.filter(is_active=True).count()
	inactive_users_count = User.objects.filter(is_active=False).count()
	total_users = active_users_count + inactive_users_count

	cane = events_details.objects.filter(apr = 0).count()
	appr = events_details.objects.filter(apr = 1).count()
	arch = events_details.objects.filter(Q(event_active = 0)&Q(apr = 1)).count()

	total_app = arch + appr
	total_events = cane + appr

	cane_percentage = 0
	appr_percentage = 0
	active_percentage = 0
	inactive_percentage = 0

	if total_users > 0:
		active_percentage = (active_users_count / total_users) * 100
		inactive_percentage = (inactive_users_count / total_users) * 100
	if total_events > 0:
		cane_percentage = (cane / total_events) * 100
		appr_percentage = (appr / total_events) * 100

	if total_app > 0:
		arch_percentage = (arch / total_app) * 100
	query = {
		's_count': User.objects.all().exclude(is_staff = True).count(),
		't_count': User.objects.all().exclude(is_staff = False).count(),
		'e_count': events_details.objects.all().count(),
		'u_count': upcoming_events,
		'ipsurl': ipsurl.objects.all(),
		'active_percentage': active_percentage,
        'inactive_percentage': inactive_percentage,
        'cane_percentage': cane_percentage,
        'appr_percentage': appr_percentage,
        'arch_percentage': arch_percentage,
        'f_count': ecert.objects.all().count(),
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
	upcoming_events = events_details.objects.filter(Q(events_schedule__gte=now)&Q(apr = 1))
	pst = events_details.objects.filter(Q(events_schedule__lt=now)&Q(apr = 1))
	belong = EventParticipants.objects.filter(attendee__user = request.user)
	ue = events_details.objects.filter(events_schedule__gte=now).first()
	start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
	end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=999999)
	evt = events_details.objects.filter(Q(events_schedule__range=(start_of_day, end_of_day))&Q(apr = 1))

	for event in upcoming_events:
		print(event.events_schedule, event.event_active)
	query = {
		'session_id': session_id,
		'now': now,
    	'upcoming_events': upcoming_events,
    	'evt': evt,
    	'pst': pst,
    	'up': UserProfile.objects.filter(user = request.user),
    	'belong': belong,
    	'ipsurl': ipsurl.objects.all(),
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
    	'ed': events_details.objects.filter(apr = 1).order_by('-events_details_id')
    }

    return render(request, 'eventapp/view_event.html', context)

def approve_event(request):
    context = {
    	'ap': events_details.objects.filter(apr = 0),
    }

    return render(request, 'eventapp/approve_event.html', context)

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

def ips(request, sid, u1, u2, tag):
    # Check if a record with the same attendee and events_details_id already exists
    existing_record = AttendanceMonitoring.objects.filter(attendee=u1 + "." + u2, events_details_id=tag, sess_id=sid).first()

    if not existing_record:
        # If no record with the same values exists, create a new record
        new_record = AttendanceMonitoring.objects.create(attendee=u1 + "." + u2, events_details_id=tag, sess_id=sid)
    else:
        # If a record already exists, you can handle this case as needed
        # For example, you can update the existing record or return an error message
        # Here, we'll just print a message for demonstration purposes
        print("Record already exists for attendee and events_details_id")

    context = {
        'sid': sid,
        'u1': u1,
        'u2': u2,
        'tag': tag,
        'mya': AttendanceMonitoring.objects.filter(Q(attendee = u1+"."+u2)&Q(events_details_id = tag))
    }

    if request.method == "POST":
    	db = ecert()
    	db.event_id = tag
    	db.attendee = request.user
    	db.feedback = request.POST.get('fb')
    	db.save()

    	return redirect('/eventapp/stu')


    return render(request, 'eventapp/ips.html', context)

def ecerts(request):
    context = {
    	'mc': ecert.objects.filter(attendee = request.user),
    	'ev': events_details.objects.all(),
    }

    return render(request, 'eventapp/ecerts.html', context)

def ecerts1(request, tag):
    context = {
    	'tag': tag,
    	'ev': events_details.objects.filter(events_details_id = tag),
    }

    return render(request, 'eventapp/ecerts1.html', context)

def attendance(request, tag):
    context = {
    	'tag': tag,
    	'at': AttendanceMonitoring.objects.filter(events_details_id = tag),
    }

    return render(request, 'eventapp/attendance.html', context)

def radar(request, tag):
    context = {
    	'tag': tag,
    	'attendee_count': AttendanceMonitoring.objects.filter(events_details_id = tag).count(),
    	'ipsurl': ipsurl.objects.all(),
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
    events = events_details.objects.filter(apr = 1)
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
        users_in_month_range = User.objects.filter(month_range_filter).exclude(is_superuser = True)

    context = {
        'users_in_month_range': users_in_month_range,
        'start_month': start_month,
        'end_month': end_month,
        'year': year,
    }

    return render(request, 'eventapp/filter_user.html', context)

def filter_event(request):
    events = events_details.objects.all()
    filtered_events = None
    start_date = None
    end_date = None

    if request.method == 'GET':
        form = DateRangeForm(request.GET)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            filtered_events = events.filter(events_schedule__range=(start_date, end_date))

    else:
        form = DateRangeForm()

    context = {
        'events': events,
        'filtered_events': filtered_events,
        'start_date': start_date,
        'end_date': end_date,
        'form': form,
    }

    return render(request, 'eventapp/filter_event.html', context)

def p_reset(request):
    if request.method == 'POST':
        emailadd = request.POST.get('eadd')
        
        try:
            user = User.objects.get(email=emailadd)
            if user:
                # Generate a reset link, you should use a proper URL
                reset_link = 'https://evmfeucavite.pythonanywhere.com/eventapp/rpo/'+str(user) # Replace with your actual reset URL

                subject = 'Reset Password'
                message = f'Good day, click on the link to reset your password: {reset_link}'
                from_email = 'evm.feu@gmail.com'  # Replace with the email you want to use as "From" address
                recipient = [emailadd]

                send_mail(subject, message, from_email, recipient, fail_silently=False)
                messages.info(request, "A link for password reset has been sent to your email address. Kindly check your email or contact the IT Administrator at (02) 0022 local 31.")

                return render(request, 'eventapp/p_reset.html')
            else:
                messages.info(request, 'Failed!')
                return render(request, 'eventapp/p_reset.html')
        except ObjectDoesNotExist:
            messages.info(request, 'Email Not Found')
            return render(request, 'eventapp/p_reset.html')

    return render(request, 'eventapp/p_reset.html')

def change_p(request):
    context = {}

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

    return render(request, 'eventapp/change_p.html', context)

def rpo(request, un):
    context = {
    	'un': un
    }

    if request.method == 'POST':
    	db = User.objects.get(username = un)
    	new_password = request.POST.get('new_password')
    	db.set_password(new_password)
    	db.save()

    	messages.success(request, 'Your password was successfully updated.')
    	return redirect('/')

    return render(request, 'eventapp/change_p.html', context)

def radar_dash(request):
    context = {

    }

    return render(request, 'eventapp/radar_dash.html', context)

def apr(request, tag):
    context = {
    	'tag': tag,
    	'exec': events_details.objects.filter(events_details_id = tag).update(apr = 1),
    }

    return render(request, 'eventapp/apr.html', context)

def fform(request, tag):
    context = {
        'tag': tag,
        'qs': qform.objects.filter(event_id = tag),
        'ecert': ecert.objects.filter(Q(attendee = request.user)&Q(event_id = tag)).first()
    }

    if request.method == "POST":
        event_id = tag
        attendee = request.user
        feedback = request.POST.get('fb')
        q1_rating = request.POST.get('rating1')
        q2_rating = request.POST.get('rating2')
        q3_rating = request.POST.get('rating3')
        q4_rating = request.POST.get('rating4')
        # Check if a record with the same event_id and attendee already exists
        existing_record = ecert.objects.filter(event_id=event_id, attendee=attendee).first()
        
        if existing_record:
            # If a record already exists, you can update the feedback or take other actions as needed
            existing_record.feedback = feedback
            existing_record.q1 = q1_rating
            existing_record.q2 = q2_rating
            existing_record.q3 = q3_rating
            existing_record.q4 = q4_rating
            existing_record.save()
        else:
            # If no record exists, create a new one
            db = ecert(event_id=event_id, attendee=attendee, feedback=feedback, q1 = q1_rating, q2 = q2_rating, q3 = q3_rating, q4 = q4_rating)
            db.save()

        return redirect('/eventapp/cw')

    return render(request, 'eventapp/fform.html', context)

def q_form(request, tag):
    if request.method == 'POST':
        form = QForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.event_id = tag
            instance.save()
    else:
        form = QForm()

    context = {
        'tag': tag,
        'form': form,
        'dis': qform.objects.filter(event_id = tag),
    }

    return render(request, 'eventapp/qform.html', context)

def ana(request, tag):
    # Get averages for the specified event_id
    basis = qform.objects.filter(event_id = tag)[:4]
    averages = ecert.objects.filter(event_id=tag).aggregate(
        avg_q1=Avg('q1'),
        avg_q2=Avg('q2'),
        avg_q3=Avg('q3'),
        avg_q4=Avg('q4'),
    )

    context = {
        'tag': tag,
        'averages': averages,
        'basis': basis,
    }

    return render(request, 'eventapp/ana.html', context)

def removeq(request, tag, ref):
    context = {
    	'tag': tag,
    	'ref': ref,
    	'exec': qform.objects.filter(id = tag).delete(),
    }

    return render(request, 'eventapp/removeq.html', context)

def deta(request, tag):
    context = {
    	'tag': tag,
    	'evt': events_details.objects.filter(events_details_id = tag),
    	'ep': EventParticipants.objects.filter(event__events_details_id = tag),
    }

    return render(request, 'eventapp/deta.html', context)