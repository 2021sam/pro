# /Users/2021sam/apps/zyxe/pro/employer_skill/forms.py

from django import forms
from django.forms import modelformset_factory, BaseInlineFormSet
from .models import EmployerSkill
from employer_job.models import EmployerJob

class EmployerSkillForm(forms.ModelForm):
    skill_years = forms.IntegerField(required=False)
    skill_months = forms.IntegerField(required=False)  # Ensure this is included

    class Meta:
        model = EmployerSkill
        fields = ['id', 'skill', 'skill_years', 'skill_months']

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

# Create a formset for EmployerSkill
EmployerSkillFormSet = modelformset_factory(EmployerSkill, form=EmployerSkillForm, extra=1)


class JobFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        # Remove empty rows where skill is blank
        for form in self.forms:
            skill = form.cleaned_data.get('skill')
            if not skill:
                # Don't raise validation errors, remove the form data
                form.cleaned_data = {}

    def save(self, commit=True):
        # Remove any forms that are effectively empty (no data in required fields)
        self.forms = [form for form in self.forms if form.cleaned_data.get('skill')]
        return super().save(commit=commit)
