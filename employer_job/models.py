# /Users/2021sam/apps/zyxe/pro/employer_job/models.py
from django.db import models
from django.utils import timezone
from django.conf import settings


class EmployerJob(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Allow multiple skills per user
    timestamp = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.title} {self.description}'
