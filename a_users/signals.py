from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from allauth.account.signals import email_changed
from allauth.account.models import EmailAddress
from .models import Profile

# This signal ensures that the username is always stored in lowercase
# for consistency and easier lookups. It runs before the User object is saved.
@receiver(pre_save, sender=User)
def user_presave(sender, instance, **kwargs):
    if instance.username:
        instance.username = instance.username.lower()

# This signal ensures a Profile object is created for every new User.
# It uses get_or_create to prevent potential race conditions or errors
# if a profile might somehow already exist (though 'created' flag should handle this).
# This is generally preferred over manual creation logic within forms or views,
# as it centralizes the profile creation logic.
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # get_or_create is robust for ensuring a profile exists for a new user
        Profile.objects.get_or_create(user=instance)

# This signal handles changes to a user's email address specifically when using django-allauth.
# It listens to allauth's 'email_changed' signal, which is triggered when an email
# address is successfully updated through allauth's mechanisms.
# When an email changes, it's crucial to mark the new email as unverified
# so that the user is prompted to re-verify their email address.
@receiver(email_changed)
def email_changed_handler(sender, request, user, from_email_address, to_email_address, **kwargs):
    # Find the newly set email address in EmailAddress model and mark it as unverified.
    # This ensures that the user has to re-confirm their new email.
    # We filter by user and the new email to ensure we're updating the correct record.
    EmailAddress.objects.filter(user=user, email=to_email_address.email).update(verified=False)

# Note: The 'save_user_profile' signal from the second snippet is omitted here.
# It was:
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     if hasattr(instance, 'profile'):
#         instance.profile.save()
# This signal is often redundant if profile updates are primarily handled via forms
# (e.g., ProfileForm, MentorProfileForm, MenteeProfileForm). If a form is used to
# update the profile, the form's save() method will explicitly save the profile.
# Having this signal would cause an extra database write every time a User object
# is saved, even if no changes were made to the related Profile.
# Only include it if you have scenarios where the User object is saved,
# and you need the related Profile to be saved implicitly without a direct call.
