# /Users/2021sam/apps/zyxe/pro/pro_experience/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from django.conf import settings



class Experience(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Allow multiple skills per user
    timestamp = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=120)

    personal_professional_project = models.BooleanField(default=False)
    company = models.CharField(max_length=50, blank=True)
    company_web = models.URLField(max_length=30, default=False)
    company_manager = models.CharField(max_length=50, blank=True)
    company_manager_phone = models.CharField(max_length=12, blank=True)
    company_manager_email = models.CharField(max_length=30, blank=True)
    recruiter = models.CharField(max_length=50, blank=True)
    recruiter_web = models.URLField(max_length=20, blank=True)
    recruiter_email = models.CharField(max_length=50, blank=True)
    recruiter_phone = models.CharField(max_length=50, blank=True)
    on_site_work_city = models.CharField(max_length=50, blank=True)
    on_site_work_state = models.CharField(max_length=50, blank=True)
    location_hybrid = models.BooleanField(default=False)
    location_remote = models.BooleanField(default=False)
    date_start = models.DateField(default=datetime.date.today)
    date_end = models.DateField(default=datetime.date.today)
    duration = models.DurationField(default=datetime.timedelta(seconds=0))
    duration_days = models.PositiveSmallIntegerField(default=0)
    hourly_pay_rate = models.FloatField(default=0)
    payment_form = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    

    def __str__(self):
        return f'{self.title} {self.company} {self.duration_days}'
    