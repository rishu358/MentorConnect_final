from django.urls import path
from a_users.views import *

urlpatterns = [
    # Put more specific patterns first
    path('register/mentor/', register_mentor, name='register-mentor'),
    path('register/mentee/', register_mentee, name='register-mentee'),
    path('onboarding/', profile_edit_view, name="profile-onboarding"),
    path('edit/', profile_edit_view, name="profile-edit"),
    path('settings/', profile_settings_view, name="profile-settings"),
    path('emailchange/', profile_emailchange, name="profile-emailchange"),
    path('emailverify/', profile_emailverify, name="profile-emailverify"),
    path('delete/', profile_delete_view, name="profile-delete"),
    path('manage/', user_management_view, name="manage-profile"),
    # Put the username pattern last as it's the most general
    path('', profile_view, name="profile"),
    path('<str:username>/', profile_view, name="profile-detail"),
]