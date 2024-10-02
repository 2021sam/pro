# /Users/2021sam/apps/zyxe/pro/authenticate/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Specify the fields to display in the user list in the Django admin
    list_display = ('username', 'email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')

    # Specify the fields that should be used in the add/change form
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('mobile_number', 'mobile_carrier')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)

# Register the CustomUserAdmin to manage CustomUser in the admin panel
admin.site.register(CustomUser, CustomUserAdmin)



from .models import CustomUser, UserSetting
# admin.site.register(UserSettings, UserSettingsAdmin)  # Manually registering the model
@admin.register(UserSetting)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'color_theme', 'receive_reminders', 'receive_alerts')
    search_fields = ('user__username', 'role')
