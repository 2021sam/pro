# /Users/2021sam/apps/zyxe/pro/employer_search/models.py

# /Users/2021sam/apps/zyxe/pro/employer_search/models.py

from django.db import models
from freelancer_profile.models import FreelancerProfile  # Importing the FreelancerProfile model

class EmployerDecision(models.Model):
    freelancer = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE, related_name='decisions')
    job_id = models.IntegerField()  # You might want to link this to a specific job model
    interested = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    decision_rating = models.PositiveSmallIntegerField(null=True, blank=True)  # 1-10 rating

    def __str__(self):
        return f"Decision for {self.freelancer} on job {self.job_id}"

    class Meta:
        verbose_name = 'Employer Decision'
        verbose_name_plural = 'Employer Decisions'
