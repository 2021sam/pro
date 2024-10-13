# /Users/2021sam/apps/zyxe/freelancer_experience/forms.py
from django import forms
from .models import FreelancerExperience, FreelancerSkill

class FreelancerExperienceForm(forms.ModelForm):
    class Meta:
        model = FreelancerExperience
        fields = ['title', 'company', 'start_date', 'end_date', 'description']

class FreelancerSkillForm(forms.ModelForm):
    class Meta:
        model = FreelancerSkill
        fields = ['skill', 'skill_years', 'skill_months']
