from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from allauth.account.utils import send_email_confirmation
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.views import redirect_to_login
from django.contrib import messages
from .forms import *

def home_view(request):
    mentors = Profile.objects.filter(user_type='MENTOR')
    context = {
        'mentors': mentors
    }
    return render(request, 'home.html', context)

def profile_view(request, username=None):
    if username:
        profile = get_object_or_404(User, username=username).profile
    else:
        try:
            profile = request.user.profile
        except:
            return redirect_to_login(request.get_full_path())
    return render(request, 'a_users/profile.html', {'profile':profile})


@login_required
def profile_edit_view(request):
    form = ProfileForm(instance=request.user.profile)  
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
        
    if request.path == reverse('profile-onboarding'):
        onboarding = True
    else:
        onboarding = False
      
    return render(request, 'a_users/profile_edit.html', { 'form':form, 'onboarding':onboarding })

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
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'a_users/profile_edit.html', {'form': form})




from django.contrib.auth import login


from django.contrib import messages  # Add this import at the top

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import MentorRegistrationForm, MenteeRegistrationForm

# a_users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import MentorRegistrationForm, MenteeRegistrationForm

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import MentorRegistrationForm, MenteeRegistrationForm  # Update these imports

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