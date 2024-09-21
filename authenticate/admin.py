from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # Define the fields to display in the admin list view
    list_display = ('email', 'mobile_number', 'mobile_carrier', 'mobile_authenticated', 'is_staff', 'is_active')

    # Fields to edit in the admin detail view
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('mobile_number', 'mobile_carrier', 'mobile_authenticated')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    # Fields to show when creating a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'mobile_number', 'mobile_carrier', 'mobile_authenticated'),
        }),
    )

    # Ordering by email in the admin
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)