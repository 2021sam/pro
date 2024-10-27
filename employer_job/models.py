# /Users/2021sam/apps/zyxe/pro/employer_job/models.py
from django.db import models
from django.utils import timezone
from django.conf import settings
from datetime import timedelta


class EmployerJob(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('cancelled', 'Cancelled'),
        ('filled', 'Filled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=50)
    job_street_address = models.CharField(max_length=30, blank=True)
    job_city = models.CharField(max_length=30, blank=True)
    job_state = models.CharField(max_length=30, blank=True)
    job_zip_code = models.CharField(max_length=30, blank=True)

    # New fields
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    start_date = models.DateField(null=True, blank=True)
    number_of_openings = models.PositiveIntegerField(default=1)
    job_post_date = models.DateField(default=timezone.now)  # Renamed from job_open_date
    job_close_date = models.DateField(null=True, blank=True)  # Optional

    # Location Preferences
    location_on_site = models.BooleanField(default=False)
    location_hybrid = models.BooleanField(default=False)
    location_remote = models.BooleanField(default=False)
    commute_limit_miles = models.PositiveSmallIntegerField(default=50)
    commute_limit_minutes = models.PositiveSmallIntegerField(default=120)

    def days_remaining_until_closed(self):
        """
        Calculates the number of days remaining until the job is closed.
        Example assumes the job remains open for 30 days from the post date.
        """
        closing_date = self.job_post_date + timedelta(days=30)
        remaining_days = (closing_date - timezone.now().date()).days
        return remaining_days if remaining_days > 0 else 0

    def number_of_applicants(self):
        """
        Counts the number of applicants who applied to this job.
        Assumes a JobApplication model exists that tracks applications.
        """
        return self.jobapplication_set.count()

    def __str__(self):
        return f'{self.title} - {self.description} ({self.status})'
