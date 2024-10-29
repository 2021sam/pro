# /Users/2021sam/apps/zyxe/pro/employer_search/admin.py

from django.contrib import admin
from .models import EmployerDecision

@admin.register(EmployerDecision)
class EmployerDecisionAdmin(admin.ModelAdmin):
    list_display = ('freelancer', 'job_id', 'interested', 'rejected', 'decision_rating')
    search_fields = ('freelancer__first_name', 'freelancer__last_name', 'job_id')
