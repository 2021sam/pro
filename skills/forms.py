from django.forms import ModelForm
from .models import Skills

class SkillsForm(ModelForm):
    class Meta:
        model = Skills
        fields = ['experience', 'skill', 'skill_years', 'skill_months']
