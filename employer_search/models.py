from django.db import models

class RecruiterJob(models.Model):
    job_title = models.CharField(max_length=255)
    job_zip_code = models.CharField(max_length=10)
    commute_limit_miles = models.IntegerField(default=30)  # Default to 30 miles commute limit
    # other job fields

class Freelancer(models.Model):
    # Assuming you pull in the freelancer model from elsewhere
    freelancer_zip_code = models.CharField(max_length=10)
    # other freelancer details
