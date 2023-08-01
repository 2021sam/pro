from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from experience.models import Experience


class Skills(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    published_at = models.DateTimeField(default=timezone.now)
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE)
    skill = models.CharField(max_length=30, blank=True, help_text = 'Note: Skills are mutually exclusive in terms of adding time to subset skills.  Furthermore, only experience time with matching terms are added.')
    skill_years = models.SmallIntegerField(default=0)
    skill_months = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'{self.experience} {self.skill} {self.skill_years} {self.skill_months}'
    