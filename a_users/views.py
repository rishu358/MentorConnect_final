from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from allauth.account.utils import send_email_confirmation
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login # Added login import here
from django.contrib.auth.models import User
from django.contrib.auth.views import redirect_to_login
from django.contrib import messages
from .forms import * # Assuming all necessary forms are imported here, including MentorRegistrationForm, MenteeRegistrationForm, ProfileForm, EmailForm

def home_view(request):
    mentors = Profile.objects.filter(user_type='MENTOR')
    context = {
        'mentors': mentors
    }
    return render(request, 'home.html', context)

def profile_view(request, username=None):
    if username:
        try:
            profile = get_object_or_404(User, username=username).profile
        except Profile.DoesNotExist:
            messages.error(request, "Profile not found.")
            return redirect('home')
    else:
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            # Create profile if it doesn't exist
            profile = Profile.objects.create(user=request.user)
    return render(request, 'a_users/profile.html', {'profile': profile})

@login_required
def profile_edit_view(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)
    
    form = ProfileForm(instance=profile)  
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
        else:
            messages.error(request, "Please correct the errors below.")
            
    onboarding = request.path == reverse('profile-onboarding')
    return render(request, 'a_users/profile_edit.html', {'form': form, 'onboarding': onboarding})

@login_required
def profile_settings_view(request):
    return render(request, 'a_users/profile_settings.html')


@login_required
def profile_emailchange(request):
    
    if request.htmx:
        form = EmailForm(instance=request.user)
        return render(request, 'partials/email_form.html', {'form':form})
    
    if request.method == 'POST':
        form = EmailForm(request.POST, instance=request.user)

        if form.is_valid():
            
            # Check if the email already exists
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exclude(id=request.user.id).exists():
                messages.warning(request, f'{email} is already in use.')
                return redirect('profile-settings')
            
            form.save() 
            
            # Then Signal updates emailaddress and set verified to False
            
            # Then send confirmation email 
            send_email_confirmation(request, request.user)
            
            return redirect('profile-settings')
        else:
            messages.warning(request, 'Form not valid')
            return redirect('profile-settings')
        
    return redirect('home')


@login_required
def profile_emailverify(request):
    send_email_confirmation(request, request.user)
    return redirect('profile-settings')


@login_required
def profile_delete_view(request):
    user = request.user
    if request.method == "POST":
        logout(request)
        user.delete()
        messages.success(request, 'Account deleted, what a pity')
        return redirect('home')
    
    return render(request, 'a_users/profile_delete.html')


@login_required
def user_management_view(request):
    # This view seems to be a duplicate or similar to profile_edit_view.
    # If it's intended for general user management (e.g., by an admin),
    # its logic would need to be different to handle other users.
    # For now, it's updated to use the same logic as profile_edit_view
    # to ensure a profile exists.
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'a_users/profile_edit.html', {'form': form})


def register_mentor(request):
    if request.method == 'POST':
        form = MentorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('profile-onboarding')
    else:
        form = MentorRegistrationForm()
    return render(request, 'account/signup.html', {
        'form': form,
        'user_type': 'Mentor'
    })

def register_mentee(request):
    if request.method == 'POST':
        form = MenteeRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('profile-onboarding')
    else:
        form = MenteeRegistrationForm()
    return render(request, 'account/signup.html', {
        'form': form,
        'user_type': 'Mentee'
    })
