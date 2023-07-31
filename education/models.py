from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
import datetime



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


class Education_Model(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    published_at = models.DateTimeField(default=timezone.now)
    school_name = models.CharField(max_length=30, blank=True)
    degree_type = models.CharField(max_length=20, choices = CHOICES_DEGREE_TYPE, default='select degree type')
    major = models.CharField(max_length=30, blank=True)
    year_graduated = models.SmallIntegerField(blank=True, null=True, validators=[MinValueValidator(2000), MaxValueValidator(2030)])
    currently_enrolled = models.BooleanField(default=False)
    gpa = models.FloatField(default=0)
