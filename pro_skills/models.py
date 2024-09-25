# /Users/2021sam/apps/zyxe/pro/pro_skills/models.py
# models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from pro_experience.models import Experience
from django.conf import settings


class Skill(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    # user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Allow multiple skills per user
    timestamp = models.DateTimeField(default=timezone.now)
    # experience = models.ForeignKey(Experience, on_delete=models.CASCADE, null=True, blank=True)  # Optional mapping
    experience = models.ManyToManyField(Experience, blank=True)
    skill = models.CharField(max_length=100)
    skill_years = models.PositiveIntegerField(default=0)  # Years of experience
    skill_months = models.PositiveIntegerField(default=0)  # Months of experience


    def __str__(self):
            experiences = ', '.join([str(exp) for exp in self.experience.all()])
            return f"{self.skill} ({self.skill_years} years, {self.skill_months} months), {experiences}"
