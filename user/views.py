from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from exam.models import *
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from django.urls import reverse
import random
from django.contrib.sessions.models import Session
from django.urls import reverse
from django.contrib.auth.hashers import make_password

# Create your views here.

@login_required(login_url='', redirect_field_name='next')
def notifications(request):
	return render(request, 'notifications.html')

def sign_in(request):
	if(request.method=='POST'):
		email = request.POST['email']
		password = request.POST['password']
		user = authenticate(email=email, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return redirect('user:dashboard')
			else:
				err= 'user account suspended'
				context={
				'error':err,
				'email':email,
				}
				return render(request, 'sign-in.html', context)
		else:
				err= 'incorrect username or password'
				context={
				'error':err,
				'email':email,
				}
				return render(request, 'sign-in.html', context)

	else:
		return render(request, 'sign-in.html')

def sign_up(request):
	if(request.method=='POST'):
		email = request.POST.get('email')
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		return_url = reverse('user:sign_up_complete', args=[email,first_name,last_name,])
		return redirect(return_url)
	return render(request, 'sign-up.html')

def sign_up_complete(request,email,first_name,last_name):
	if(request.method=='POST'):
		bvn = request.POST.get('bvn')
		nin = request.POST.get('nin')
		home = request.POST.get('home')
		number = request.POST.get('number')
		gender = request.POST.get('gender')
		marital = request.POST.get('marital')
		nwApplication = UserApplication(Email=email, First_name=first_name,Last_name=last_name,Bvn=bvn,Nin=nin,Home_address=home,Gender=gender, Marital_status=marital, Phone_number=number)
		nwApplication.save()
		return redirect('user:sign_up_success')
	return render(request, 'sign-up-complete.html')

def sign_up_success(request):
	return render(request, 'sign-up-success.html')

@login_required(login_url='', redirect_field_name='next')
def sign_out(request):
	user = request.user
	logout(request)
	return redirect('user:sign_in')

def home(request):
	if (request.method=='POST'):
		passcode = request.POST.get('passcode')
		return_url = reverse('exam:welcome', args=[passcode])
		return redirect(return_url)
	return render(request,'home.html')