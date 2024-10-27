# /Users/2021sam/apps/zyxe/pro/employer_job/forms.py
from django import forms
from .models import EmployerJob

class EmployerJobForm(forms.ModelForm):
    class Meta:
        model = EmployerJob
        fields = ['title', 'description', 'job_street_address', 'job_city', 'job_state', 'job_zip_code',
                  'status', 'start_date', 'number_of_openings', 'job_post_date', 'job_close_date',
                  'location_on_site', 'location_hybrid', 'location_remote', 'commute_limit_miles', 'commute_limit_minutes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Disable job_post_date and job_close_date if the job already exists (edit case)
        if self.instance.pk:  # Check if this is an existing job (edit mode)
            self.fields['job_post_date'].disabled = True
            self.fields['job_close_date'].disabled = True


# from django.forms import ModelForm
# from .models import EmployerJob

# class EmployerJobForm(ModelForm):
#     class Meta:
#         model = EmployerJob
#         fields = ['job_post_date', 'job_close_date', 'status', 'start_date', 'title', 'description', 'job_street_address', 'job_city', 'job_state', 'job_zip_code', 'commute_limit_miles']
