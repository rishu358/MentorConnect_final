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
        fields = ['image', 'displayname', 'info']
        labels = {
            'image': 'Profile Picture',
            'displayname': 'Display Name',
            'info': 'About Me'
        }
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'displayname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your display name'
            }),
            'info': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Tell us about yourself'
            })
        }

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

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Create profile after user is saved
            Profile.objects.get_or_create(
                user=user,
                defaults={'user_type': 'MENTEE'}
            )
        return user