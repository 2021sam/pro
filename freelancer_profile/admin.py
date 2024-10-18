from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'user', 'date_of_birth', 'desired_job_title', 'desired_salary', 'desired_hourly_rate')
    search_fields = ('user__username', 'desired_job_title')
    list_filter = ('date_of_birth', 'desired_salary', 'desired_hourly_rate')
    ordering = ('user',)

    # You can customize the form layout or fieldsets here if needed
    fieldsets = (
        (None, {
            'fields': ('user', 'date_of_birth', 'desired_job_title', 'desired_salary', 'desired_hourly_rate')
        }),
        ('Contact Information', {
            'fields': ('mobile_cell_number', 'linkedin', 'portfolio')
        }),
        ('Location Preferences', {
            'fields': ('residential_street_address', 'residential_city_address', 'residential_state_address', 'residential_zip_address')
        }),
        ('Travel Preferences', {
            'fields': ('travel_preference', 'willing_to_relocate')
        }),
    )

    # Custom method to display the user_id
    def user_id(self, obj):
        return obj.user.id

    # Set column title for user_id
    user_id.short_description = 'User ID'

# Optionally, register other models if they exist
