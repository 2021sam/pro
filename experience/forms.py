from django.forms import ModelForm
from .models import Experience

class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = ['title', 'company', 'personal_professional_project', 'company_manager', 'recruiter', 'recruiter_email', 'on_site_work_city', 'on_site_work_state', 'date_start', 'date_end', 'duration', 'description', 'hourly_pay_rate']
        