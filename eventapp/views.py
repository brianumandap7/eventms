from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.models import User

def admindash(request):
	query = {
		
	}
	return render(request, 'eventapp/admindash.html', query)

def stu(request):
	query = {
		
	}
	return render(request, 'eventapp/admindash.html', query)

def sao(request):
	query = {
		
	}
	return render(request, 'eventapp/sao.html', query)

# Create your views here.
