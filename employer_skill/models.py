# /Users/2021sam/apps/zyxe/pro/employer_skill/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from employer_job.models import EmployerJob
from django.conf import settings


class EmployerSkill(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Allow multiple skills per user
    timestamp = models.DateTimeField(default=timezone.now)
    job = models.ForeignKey(EmployerJob, on_delete=models.CASCADE)
    skill = models.CharField(max_length=100)
    skill_years = models.PositiveIntegerField(default=0)  # Years of experience
    skill_months = models.PositiveIntegerField(default=0)

def __str__(self):
    return f"{self.skill} ({self.skill_years} years, {self.job}"
