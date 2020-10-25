from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.conf import settings
from django.core import mail
from django.contrib.auth import login, authenticate

from teacher import views
from administrator import views

def home(request):
    return render(request, 'users/login.html')
	
def password_reset(request):
	return render(request, 'users/password_reset.html')

def success(request):
	if request.user.is_staff:
		return redirect('administrator-home')
	return redirect('teacher-home')