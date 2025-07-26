from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'displayname', 'user_type', 'working_status', 'organization']
    list_filter = ['user_type', 'working_status', 'terms_accepted']
    search_fields = ['user__username', 'user__email', 'displayname', 'organization']
    readonly_fields = ['user']