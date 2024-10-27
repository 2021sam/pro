# /Users/2021sam/apps/zyxe/pro/employer_job/models.py
from django.db import models
from django.utils import timezone
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

    # Status and Dates
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    start_date = models.DateField(null=True, blank=True)
    number_of_openings = models.PositiveIntegerField(default=1)

    # Allow user to set these on creation, but prevent changes later
    job_post_date = models.DateField(default=timezone.now)
    job_close_date = models.DateField(null=True, blank=True)

    # Location Preferences
    location_on_site = models.BooleanField(default=False)
    location_hybrid = models.BooleanField(default=False)
    location_remote = models.BooleanField(default=False)
    commute_limit_miles = models.PositiveSmallIntegerField(default=50)
    commute_limit_minutes = models.PositiveSmallIntegerField(default=120)

    def save(self, *args, **kwargs):
        """
        Ensure that job_post_date and job_close_date are set only once during job creation.
        They cannot be changed once the job has been created.
        """
        # If the job is being updated (i.e., not the first save), prevent changes to post and close dates
        if self.pk:  # This means the job already exists
            original = EmployerJob.objects.get(pk=self.pk)
            self.job_post_date = original.job_post_date
            self.job_close_date = original.job_close_date

        # If no job_close_date is provided, default to 30 days after post date on creation
        if not self.job_close_date:
            self.job_close_date = self.job_post_date + timedelta(days=30)

        super().save(*args, **kwargs)

    def days_remaining_until_closed(self):
        """
        Calculates the number of days remaining until the job is closed.
        """
        remaining_days = (self.job_close_date - timezone.now().date()).days
        return remaining_days if remaining_days > 0 else 0

    def __str__(self):
        return f'{self.title} - {self.status} | {self.number_of_openings} openings | Posted: {self.job_post_date}'
