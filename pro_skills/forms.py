# /Users/2021sam/apps/zyxe/pro/pro_skills/forms.py
from django import forms
from django.forms import modelformset_factory
from .models import Skill
from pro_experience.models import Experience

class SkillForm(forms.ModelForm):
    skill_years = forms.IntegerField(required=False)
    skill_months = forms.IntegerField(required=False)

    # experience = forms.ModelMultipleChoiceField(
    #     queryset=Experience.objects.all(),
    #     widget=forms.CheckboxSelectMultiple,  # Use SelectMultiple if you prefer dropdown
    #     required=False
    # )

    class Meta:
        model = Skill
        fields = ['skill', 'skill_years', 'skill_months', 'experience']

    def clean(self):
        cleaned_data = super().clean()
        skill_years = cleaned_data.get('skill_years', 0)
        skill_months = cleaned_data.get('skill_months', 0)

        # Ensure at least one of skill_years or skill_months is filled
        if skill_years == 0 and skill_months == 0:
            raise forms.ValidationError("At least one of 'Skill Years' or 'Skill Months' must be filled.")

        # Return 0 for blank fields instead of None
        cleaned_data['skill_years'] = skill_years if skill_years is not None else 0
        cleaned_data['skill_months'] = skill_months if skill_months is not None else 0

        return cleaned_data

SkillFormSet = modelformset_factory(Skill, form=SkillForm, extra=1)
