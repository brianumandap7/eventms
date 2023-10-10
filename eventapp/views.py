from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.contrib.auth.models import User
from .forms import EventsDetailsForm, EventsDetailsEditForm, CustomUserCreationForm, CustomUserEditForm
from .models import events_details, UserProfile, AttendanceMonitoring, UserLogs
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



def admindash(request):
	query = {
		's_count': User.objects.all().exclude(is_staff = True).count(),
		't_count': User.objects.all().exclude(is_staff = False).count(),
		'e_count': events_details.objects.all().count(),
	}
	return render(request, 'eventapp/admindash.html', query)

def stu(request):

	session_id = request.session.session_key
	query = {
		'session_id': session_id,
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
    	'ed': events_details.objects.all()
    }

    return render(request, 'eventapp/create_event.html', context)

def view_event(request):
    context = {
    	'ed': events_details.objects.all()
    }

    return render(request, 'eventapp/view_event.html', context)


def edit_event(request, event_id):
    event = get_object_or_404(events_details, pk=event_id)

    if request.method == 'POST':
        form = EventsDetailsEditForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            # Optionally, you can redirect to a success page or display a message
            messages.success(request, 'Event updated successfully.')
            return redirect('/eventapp/view_event')   # Change 'success_page' to the actual URL name
    else:
        form = EventsDetailsEditForm(instance=event)

    return render(request, 'eventapp/edit_event.html', {'form': form, 'event': event})

def ar(request, tag):
    context = {
    	'tag': tag,
    	'exec': events_details.objects.filter(events_details_id = tag).update(event_active = 0),
    }

    return render(request, 'eventapp/ar.html', context)

def ua(request, tag):
    context = {
    	'tag': tag,
    	'exec': events_details.objects.filter(events_details_id = tag).update(event_active = 1),
    }

    return render(request, 'eventapp/ua.html', context)

def manage_users(request):
    context = {
    	'all_users': User.objects.all().exclude(is_superuser = True),
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
    context = {
    	'tag': tag,
    	'un': un,
    	'ulogs': UserLogs.objects.filter(user = un),
    	'us': User.objects.filter(id = tag),
    }

    return render(request, 'eventapp/user_logs.html', context)

def hist(request, tag):
    context = {
    	'tag': tag,
    	'ev': events_details.objects.filter(events_details_id = tag),
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
        return HttpResponseRedirect('/eventapp/manage_users/')
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


