# /Users/2021sam/apps/zyxe/pro/pro_skills/forms.py
from django import forms
from django.forms import modelformset_factory
from .models import Skill
from pro_experience.models import Experience

class SkillForm(forms.ModelForm):
    experience = forms.ModelMultipleChoiceField(
        queryset=Experience.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # Use SelectMultiple if you prefer dropdown
        required=False
    )
    skill_years = forms.IntegerField(required=False, min_value=0)
    skill_months = forms.IntegerField(required=False, min_value=0)

    class Meta:
        model = Skill
        fields = ['skill', 'skill_years', 'skill_months', 'experience']

    def clean(self):
        cleaned_data = super().clean()
        skill_years = cleaned_data.get('skill_years')
        skill_months = cleaned_data.get('skill_months')
        #
        # # Ensure at least one of skill_years or skill_months is filled
        # if skill_years == 0 and skill_months == 0:
        #     raise forms.ValidationError("At least one of 'Skill Years' or 'Skill Months' must be filled.")

        # If both are empty or both are 0, raise validation error
        if (skill_years is None or skill_years == 0) and (skill_months is None or skill_months == 0):
            raise forms.ValidationError(
                "At least one of 'Skill Years' or 'Skill Months' must be filled with a non-zero value.")

        return cleaned_data

SkillFormSet = modelformset_factory(Skill, form=SkillForm, extra=1)
