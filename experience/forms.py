from django.forms import ModelForm
from .models import Experience

class PostForm(ModelForm):
    class Meta:
        model = Experience
        fields = ['title', 'company', 'company_manager', 'recruiter', 'recruiter_email', 'city', 'state', 'date_start', 'date_end', 'duration', 'description', 'skill1', 'skill1_years', 'skill1_months', 'skill2', 'skill2_years', 'skill2_months', 'skill3', 'skill3_years', 'skill3_months', 'hourly_pay_rate']
        