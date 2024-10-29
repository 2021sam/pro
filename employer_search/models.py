# /Users/2021sam/apps/zyxe/pro/employer_search/models.py

from django.db import models
from freelancer_profile.models import FreelancerProfile
from employer_job.models import EmployerJob


class EmployerDecision(models.Model):
    DECISION_CHOICES = [
        ('interested', 'Interested'),
        ('reject', 'Reject'),
    ]

    job = models.ForeignKey(EmployerJob, on_delete=models.CASCADE)
    freelancer = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE)
    decision = models.CharField(max_length=20, choices=DECISION_CHOICES, blank=True)
    rating = models.PositiveSmallIntegerField(null=True, blank=True, help_text="Rate the freelancer (1-10)")
    feedback = models.TextField(blank=True)

    def __str__(self):
        return f"{self.job} - {self.freelancer} decision"
