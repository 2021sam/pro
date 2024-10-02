# # Users/2021sam/apps/zyxe/pro/employer_skill/models.py
# /Users/2021sam/apps/zyxe/pro/pro_skills/models.py
# models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from pro_experience.models import Experience
from django.conf import settings


class Skill(models.Model):
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






# # Required skills for job opportunity

# from django.contrib.auth.models import User
# from django.utils import timezone
# from django.db import models
# from job.models import EmployerJob

# class EmployerSkill(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     job = models.ForeignKey(Job, on_delete=models.CASCADE)
#     timestamp = models.DateTimeField(default=timezone.now)
#     skill = models.CharField(max_length=30)
#     skill_years = models.PositiveSmallIntegerField(default=0)
#     skill_months = models.PositiveSmallIntegerField(default=0)

#     def __str__(self):
#         return f'{self.user} {self.timestamp} {self.skill}'
