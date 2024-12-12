from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    USER_TYPES = (
        ('MENTOR', 'Mentor'),
        ('MENTEE', 'Mentee'),
    )
    
    WORKING_STATUS_CHOICES = (
        ('EMPLOYED', 'Employed'),
        ('SELF_EMPLOYED', 'Self Employed'),
        ('UNEMPLOYED', 'Unemployed'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='avatars/', null=True, blank=True)
    displayname = models.CharField(max_length=20, null=True, blank=True)
    info = models.TextField(null=True, blank=True)
    
    # Add new fields
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    working_status = models.CharField(
        max_length=20, 
        choices=WORKING_STATUS_CHOICES,
        null=True,
        blank=True
    )
    organization = models.CharField(max_length=100, null=True, blank=True)
    designation = models.CharField(max_length=100, null=True, blank=True)
    linkedin_url = models.URLField(max_length=200, null=True, blank=True)
    github_url = models.URLField(max_length=200, null=True, blank=True)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    terms_accepted = models.BooleanField(default=False)
    user_type = models.CharField(max_length=6, choices=USER_TYPES, default='MENTEE')

    def __str__(self):
        return str(self.user)

    @property
    def name(self):
        return self.displayname or self.user.username

    @property
    def avatar(self):
        if self.image:
            return self.image.url
        return '/static/images/avatar.png'