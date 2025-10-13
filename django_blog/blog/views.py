from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth import login
# Create your views here.

def home(request):
    return render(request, 'blog/home.html')

def register(request):
	if request.method == 'POST':
		form = CustomUserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			Profile.objects.get_or_create(user=user)
			login(request, user)
			messages.success(request, "Registration successful. You're now logged in.")
			return redirect('home')
		else:
			messages.error(request, "Please correct the errors below.")
	else:
		form = CustomUserCreationForm()
	return render(request, 'blog/register.html', {'form': form})

@login_required
def profile_view(request):
	profile, _ = Profile.objects.get_or_create(user=request.user)
	if request.method == 'POST':
		form = ProfileForm(request.POST, instance=profile)
		if form.is_valid():
			form.save()
			new_email = request.POST.get('email', '').strip()
			if new_email and new_email != request.user.email:
				request.user.email = new_email
				request.user.save()
			messages.success(request, "Profile updated successfully.")
			return redirect('profile')
		else:
			messages.error(request, "Please correct the errors below.")
	else:
		form = ProfileForm(instance=profile)
	return render(request, 'blog/profile.html', {'form': form})
