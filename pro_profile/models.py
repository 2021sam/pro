# /Users/2021sam/apps/zyxe/pro/pro_profile/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings

CHOICES_WORK_AUTHORIZATION = (
    ('select work authorization', 'Select Work Authorization'),
    ('us_citizen', 'US Citizen'),
    ('canadian_citizen', 'Canadian Citizen'),
    ('Have H1 Visa', 'Have H1 Visa'),
    ('Need H1 Visa', 'Need H1 Visa'),
    ('Green Card Holder', 'Green Card Holder'),
    ('TN Permit Holder', 'TN Permit Holder'),
    ('Employment Authourization Document', 'Employment Authorization Document')
)

# Create your models here.
class Profile(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    # address = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True, help_text='Please use the following format: <em>YYYY-MM-DD</em>.')
    # birth_month = models.IntegerField(blank=True, min_value=1, max_value=12)
    birth_month = models.PositiveSmallIntegerField(blank=True, null=True, validators=[MinValueValidator(1), MaxValueValidator(12)])
    birth_day = models.PositiveSmallIntegerField(blank=True, null=True, validators=[MinValueValidator(1), MaxValueValidator(31)])
    ip1 = models.TextField(max_length=46, blank=True)
    ip2 = models.TextField(max_length=46, blank=True)
    mac1 = models.TextField(max_length=50, blank=True)
    mac2 = models.TextField(max_length=50, blank=True)
    drivers_license = models.TextField(max_length=30, blank=True)
    linkedin = models.TextField(max_length=50, blank=True)
    portfolio = models.TextField(max_length=50, blank=True)
    residential_street_address = models.TextField(max_length=50, blank=True)
    residential_city_address = models.TextField(max_length=50, blank=True)
    residential_state_address = models.TextField(max_length=50, blank=True)
    residential_zip_address = models.TextField(max_length=50, blank=True)
    company = models.TextField(max_length=50, blank=True)
    company_web_site = models.TextField(max_length=50, blank=True)
    work_street_address = models.TextField(max_length=50, blank=True)
    work_city_address = models.TextField(max_length=50, blank=True)
    work_state_address = models.TextField(max_length=50, blank=True)
    work_zip_address = models.TextField(max_length=50, blank=True)
    mobile_cell_number = models.TextField(max_length=14, blank=True)
    willing_to_relocate = models.BooleanField(default=False)
    # (456) 456-1234       Will need to format.
    work_authorization = models.CharField(max_length=34, choices=CHOICES_WORK_AUTHORIZATION, default='select work authorization')
    open_to_public = models.BooleanField(default=False)
    # https://stackoverflow.com/questions/51623747/django-best-way-to-create-a-multiple-choice-field
    def __str__(self):
        return f'{self.id} {self.user}, {self.linkedin}'

#this method to generate profile when user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

#this method to update profile when user is updated
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()