from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.models import User

def admindash(request):
	query = {
		's_count': User.objects.all().exclude(is_staff = True).count(),
		't_count': User.objects.all().exclude(is_staff = False).count()
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

# Create your views here.