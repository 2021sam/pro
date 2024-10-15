# /Users/2021sam/apps/zyxe/freelancer_experience/forms.py
from django import forms
from django.forms import modelformset_factory 
from .models import FreelancerExperience, FreelancerSkill
from django.core.exceptions import ValidationError

class FreelancerExperienceForm(forms.ModelForm):
    class Meta:
        model = FreelancerExperience
        fields = ['title', 'company', 'date_start', 'date_end', 'description']

# class FreelancerSkillForm(forms.ModelForm):
#     class Meta:
#         model = FreelancerSkill
#         fields = ['skill', 'skill_years', 'skill_months']


class FreelancerSkillForm(forms.ModelForm):
    # skill_years = forms.IntegerField(required=False, initial=0)
    # skill_months = forms.IntegerField(required=False, initial=0)

    class Meta:
        model = FreelancerSkill
        fields = ['skill', 'skill_years', 'skill_months']

    def clean(self):
        cleaned_data = super().clean()
        skill = cleaned_data.get('skill')
        skill_years = cleaned_data.get('skill_years', 0)
        skill_months = cleaned_data.get('skill_months', 0)

        # Ensure that at least the skill field is filled
        if not skill:
            raise ValidationError("Please provide a skill.")
        
        # # Ensure that either years or months is set, or set both to 0
        if skill and skill_years == 0 and skill_months == 0:
            raise ValidationError("Please provide years or months of experience.")

        return cleaned_data
