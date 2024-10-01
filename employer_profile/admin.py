from django.contrib import admin
from .models import EmployerProfile

class EmployerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'linkedin')

admin.site.register(EmployerProfile, EmployerProfileAdmin)
