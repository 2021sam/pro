from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.conf import settings

CHOICES_DEGREE_TYPE = (
    ('select degree type', 'Select Degree Type'),
    ('none', 'None'),
    ('vocational', 'Vocational'),
    ('high school', 'High School'),
    ('associates degree', 'Associate\'s Degree'),
    ('bachelors degree', 'Bachelor\'s Degree'),
    ('masters degree', 'Master\'s Degree'),
    ('ged', 'GED')
)


class Education(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    school_name = models.CharField(max_length=30, blank=True)
    school_web_site = models.URLField(max_length=50, blank=True)
    degree_type = models.CharField(max_length=20, choices = CHOICES_DEGREE_TYPE, default='select degree type')
    major = models.CharField(max_length=30, blank=True)
    year_graduated = models.SmallIntegerField(blank=True, null=True, validators=[MinValueValidator(1980), MaxValueValidator(2030)])
    currently_enrolled = models.BooleanField(default=False)
    gpa = models.FloatField(default=0)
