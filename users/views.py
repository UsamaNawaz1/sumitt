from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages 
from django.urls import reverse_lazy
from django.views import generic
from .forms import SignUpForm, EditProfileForm
from django.http import HttpResponse

# def home(request):
# 	plans = Plan.objects
# 	return render(request, 'home.html', {})
	# return render(request, 'users/home.html', {})

def login_user(request):		
	if request.user.is_authenticated:
		return redirect('dashboard')
		
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, ('You Have Been Logged In!'))
			# return redirect('dashboard')
			if request.POST["next"]:
				return redirect(request.POST.get('next','dashboard'))
			return redirect('dashboard')

		else:
			messages.success(request, ('Error Logging In - Please Try Again...'))
			return redirect('login')
	else:
		return render(request, 'users/login.html', {})

def logout_user(request):
	logout(request)
	messages.success(request, ('You Have Been Logged Out...'))
	return redirect('home')

def register_user(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, ('You Have Been Registered...'))
			return redirect('dashboard')
	else:
		form = SignUpForm()
	
	context = {'form': form}
	return render(request, 'users/register.html', context)



def edit_profile(request):
	page = "edit_profile"
	if request.method == 'POST':
		form = EditProfileForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			messages.success(request, ('You Have Edited Your Profile...'))
			return redirect('dashboard')
	else:
		form = EditProfileForm(instance=request.user)
	
	context = {'form': form,'page':page}
	return render(request, 'users/edit_profile.html', context)

def change_password(request):
	page = "password"
	if request.method == 'POST':
		form = PasswordChangeForm(data=request.POST, user=request.user)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			messages.success(request, ('You Have Edited Your Password...'))
			return redirect('dashboard')
	else:
		form = PasswordChangeForm(user=request.user)
	
	context = {'form': form,'page':page}
	return render(request, 'users/change_password.html', context)



# Create your views here.
