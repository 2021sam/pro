from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from experience.models import Experience


class Skill(models.Model):
    # id = models.AutoField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE)
    skill = models.CharField(max_length=30)
    skill_years = models.SmallIntegerField(default=0)
    skill_months = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'{self.experience} {self.skill} {self.skill_years} {self.skill_months}'
    