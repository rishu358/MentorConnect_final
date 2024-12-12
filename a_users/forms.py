from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from allauth.account.forms import SignupForm

class MentorRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                user_type='MENTOR'
            )
        return user

class MentorRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Check if profile exists before creating
            if not hasattr(user, 'profile'):
                Profile.objects.create(
                    user=user,
                    user_type='MENTOR'
                )
        return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'displayname', 'info', 'linkedin_url', 'github_url', 'resume', 'terms_accepted']
        widgets = {
            'linkedin_url': forms.URLInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm'}),
            'github_url': forms.URLInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm'}),
            'terms_accepted': forms.CheckboxInput(attrs={'class': 'rounded border-gray-300'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['github_url'].required = False

class EmailForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['email']

class MenteeRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                user_type='MENTEE'
            )
        return user
    
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'working_status', 'organization', 'designation', 
                 'linkedin_url', 'github_url', 'resume', 'terms_accepted']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['github_url'].required = False
        self.fields['organization'].required = False
        self.fields['designation'].required = False
        
    def clean(self):
        cleaned_data = super().clean()
        working_status = cleaned_data.get('working_status')
        organization = cleaned_data.get('organization')
        designation = cleaned_data.get('designation')
        
        if working_status in ['EMPLOYED', 'SELF_EMPLOYED']:
            if not organization:
                raise forms.ValidationError("Organization is required for employed status")
            if not designation:
                raise forms.ValidationError("Designation is required for employed status")
            

class MentorProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'displayname', 'info', 'working_status', 'organization', 
                 'designation', 'linkedin_url', 'github_url', 'resume', 'terms_accepted']
        labels = {
            'image': 'Profile Picture',
            'displayname': 'Display Name',
            'info': 'Bio',
            'working_status': 'Working Status',
            'organization': 'Organization',
            'designation': 'Designation',
            'linkedin_url': 'LinkedIn URL',
            'github_url': 'GitHub URL (Optional)',
            'resume': 'Resume',
            'terms_accepted': 'Terms and Conditions'
        }

class MenteeProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'displayname', 'info']
        labels = {
            'image': 'Profile Picture',
            'displayname': 'Display Name',
            'info': 'Bio'
        }