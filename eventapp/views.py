from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.contrib.auth.models import User
from .forms import EventsDetailsForm, EventsDetailsEditForm, CustomUserCreationForm, CustomUserEditForm
from .models import events_details, UserProfile
from django.contrib import messages



def admindash(request):
	query = {
		's_count': User.objects.all().exclude(is_staff = True).count(),
		't_count': User.objects.all().exclude(is_staff = False).count(),
		'e_count': events_details.objects.all().count(),
	}
	return render(request, 'eventapp/admindash.html', query)

def stu(request):
	query = {
		
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
            messages.success(request, 'User updated successfully.')
            return redirect('/eventapp/manage_users')  # Replace 'success_page' with your desired URL
    else:
        form = CustomUserEditForm(instance=user)

    return render(request, 'eventapp/edit_profile.html', {'form': form})

def deact(request, tag):
    context = {
    	'tag': tag,
    	'exec': User.objects.filter(id = tag).update(is_active = False),
    }

    return render(request, 'eventapp/deact.html', context)

def activate(request, tag):
    context = {
    	'tag': tag,
    	'exec': User.objects.filter(id = tag).update(is_active = True),
    }

    return render(request, 'eventapp/activate.html', context)

