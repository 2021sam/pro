# /Users/2021sam/apps/zyxe/pro/employer_job/forms.py
from django.forms import ModelForm
from .models import EmployerJob


class EmployerJobForm(ModelForm):
    class Meta:
        model = EmployerJob
        fields = ['title', 'description']
