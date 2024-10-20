# /Users/2021sam/apps/zyxe/pro/employer_job/models.py
from django.db import models
from django.utils import timezone
from django.conf import settings


class EmployerJob(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Allow multiple skills per user
    timestamp = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=50)
    job_street_address = models.CharField(max_length=30, blank=True)
    job_city = models.CharField(max_length=30, blank=True)
    job_state = models.CharField(max_length=30, blank=True)
    job_zip_code = models.CharField(max_length=30, blank=True)

    # Location Preferences
    location_on_site = models.BooleanField(default=False)
    location_hybrid = models.BooleanField(default=False)
    location_remote = models.BooleanField(default=False)
    commute_limit_miles = models.PositiveSmallIntegerField(default=50)
    # commute_limit_minutes = models.PositiveSmallIntegerField(default=120)


    def __str__(self):
        return f'{self.title} {self.description}'
