from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib.auth.models import User
from .forms import EventsDetailsForm
from django.contrib import messages
from .models import events_details


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
            return redirect('/')  # Change 'success_page' to the actual URL name
    else:
        form = EventsDetailsForm(user=request.user)

    return render(request, 'eventapp/create_event.html', {'form': form})



# Create your views here.
