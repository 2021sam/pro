# /Users/2021sam/apps/zyxe/freelancer_experience/models.py
from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.utils import timezone
from django.conf import settings

class FreelancerProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Link experience to a user
    bio = models.TextField(blank=True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.BooleanField(default=True)
    location = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username


from django.db import models
from django.utils import timezone
import datetime
from django.conf import settings
# pip install django-phonenumber-field
from phonenumber_field.modelfields import PhoneNumberField

class FreelancerExperience(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Link experience to a user
    timestamp = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=120)

    personal_professional_project = models.BooleanField(default=False)
    company = models.CharField(max_length=50, blank=True)
    company_web = models.URLField(max_length=30, blank=True, default='')
    company_manager = models.CharField(max_length=50, blank=True)
    company_manager_phone = PhoneNumberField(blank=True)
    company_manager_email = models.EmailField(max_length=30, blank=True)

    recruiter = models.CharField(max_length=50, blank=True)
    recruiter_web = models.URLField(max_length=20, blank=True, default='')
    recruiter_email = models.EmailField(max_length=50, blank=True)
    recruiter_phone = PhoneNumberField(blank=True)

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
        return f'{self.title} {self.company} ({self.duration_days} days)'

    def clean(self):
        # pass
        if self.date_end < self.date_start:
            raise ValidationError('End date cannot be before the start date')





class FreelancerSkill(models.Model):
    experience = models.ForeignKey(FreelancerExperience, on_delete=models.CASCADE)
    skill = models.CharField(max_length=100)
    skill_years = models.PositiveIntegerField(default=0)
    skill_months = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.skill
