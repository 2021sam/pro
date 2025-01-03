# /Users/2021sam/apps/zyxe/pro/freelancer_profile/models.py
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings

# Choice fields
CHOICES_WORK_AUTHORIZATION = (
    ('select work authorization', 'Select Work Authorization'),
    ('us_citizen', 'US Citizen'),
    ('canadian_citizen', 'Canadian Citizen'),
    ('Have H1 Visa', 'Have H1 Visa'),
    ('Need H1 Visa', 'Need H1 Visa'),
    ('Green Card Holder', 'Green Card Holder'),
    ('TN Permit Holder', 'TN Permit Holder'),
    ('Employment Authorization Document', 'Employment Authorization Document')
)

OPEN_TO_HIRE_CHOICES = [
    ('recruiter', 'Open to Recruiter'),
    ('direct_hire', 'Direct Company Hire Only'),
]


# Validator for travel preferences
def validate_travel_preference(value):
    """Ensure the value is a multiple of 10 between 0 and 100."""
    if value % 10 != 0 or value < 0 or value > 100:
        raise ValidationError(
            f'{value} is not a valid travel percentage. It must be a multiple of 10 between 0 and 100.'
        )


# Profile Model
class FreelancerProfile(models.Model):
    # Basic Information
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='freelancer_profile')
    timestamp = models.DateTimeField(default=timezone.now)
    date_of_birth = models.DateField(null=True, blank=True, help_text='Please use the following format: <em>YYYY-MM-DD</em>.')
    # birth_date = models.DateField(null=True, blank=True, help_text='Please use the following format: <em>YYYY-MM-DD</em>.')
    birth_month = models.PositiveSmallIntegerField(blank=True, null=True,
                                                   validators=[MinValueValidator(1), MaxValueValidator(12)])
    birth_day = models.PositiveSmallIntegerField(blank=True, null=True,
                                                 validators=[MinValueValidator(1), MaxValueValidator(31)])
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.CharField(max_length=30, blank=True)
    phone_number = models.CharField(max_length=14, blank=True)

    # Contact Information
    ip1 = models.CharField(max_length=46, blank=True)
    ip2 = models.CharField(max_length=46, blank=True)
    mac1 = models.CharField(max_length=50, blank=True)
    mac2 = models.CharField(max_length=50, blank=True)
    mobile_cell_number = models.CharField(max_length=14, blank=True)
    linkedin = models.CharField(max_length=50, blank=True)
    portfolio = models.CharField(max_length=50, blank=True)

    # Residential and Work Address
    residential_street = models.CharField(max_length=50, blank=True)
    residential_city = models.CharField(max_length=50, blank=True)
    residential_state = models.CharField(max_length=50, blank=True)
    residential_zip_code = models.CharField(max_length=50, blank=True)  # Updated field name

    work_street = models.CharField(max_length=50, blank=True)
    work_city = models.CharField(max_length=50, blank=True)
    work_state = models.CharField(max_length=50, blank=True)
    work_zip_code = models.CharField(max_length=50, blank=True)  # Updated field name

    # Employment Preferences
    desired_job_title = models.CharField(max_length=50, blank=True)
    desired_salary = models.PositiveSmallIntegerField(blank=True, null=True,
                                                      validators=[MinValueValidator(1), MaxValueValidator(20)])
    desired_hourly_rate = models.SmallIntegerField(blank=True, null=True,
                                                   validators=[MinValueValidator(1), MaxValueValidator(20)])

    # Hiring Preference
    open_to_hire = models.CharField(
        max_length=20,
        choices=OPEN_TO_HIRE_CHOICES,
        default='recruiter',
        help_text='Select whether you are open to working with a recruiter or direct company hire only'
    )

    # Employment Type Preferences (Boolean Fields)
    temporary = models.BooleanField(default=False)
    permanent = models.BooleanField(default=False)
    contract = models.BooleanField(default=False)
    full_time = models.BooleanField(default=False)
    part_time = models.BooleanField(default=False)
    self_employed = models.BooleanField(default=False)
    freelance = models.BooleanField(default=False)
    apprenticeship = models.BooleanField(default=False)
    internship = models.BooleanField(default=False)
    seasonal = models.BooleanField(default=False)
    contract_corp_to_corp = models.BooleanField(default=False)
    contract_independent = models.BooleanField(default=False)
    contract_w2 = models.BooleanField(default=False)
    contract_to_hire = models.BooleanField(default=False)

    # Location Preferences
    location_on_site = models.BooleanField(default=False)
    location_hybrid = models.BooleanField(default=False)
    location_remote = models.BooleanField(default=False)
    commute_limit_miles = models.PositiveSmallIntegerField(default=50)
    commute_limit_minutes = models.PositiveSmallIntegerField(default=120)

    # Travel Preference
    travel_preference = models.IntegerField(
        default=0,
        validators=[validate_travel_preference, MinValueValidator(0), MaxValueValidator(100)],
        help_text="Specify travel preference as a percentage in increments of 10%."
    )

    willing_to_relocate = models.BooleanField(default=False)
    work_authorization = models.CharField(max_length=34, choices=CHOICES_WORK_AUTHORIZATION,
                                          default='select work authorization')
    open_to_public = models.BooleanField(default=False)

    def __str__(self):
        return f'ID: {self.id}, USER_ID: {self.user.id}, USER: {self.user}'


# Signal Handlers
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        FreelancerProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
