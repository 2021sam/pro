from django import forms
from django.forms import modelformset_factory, BaseInlineFormSet
from .models import EmployerSkill
from employer_job.models import EmployerJob

# EmployerSkillForm handles the fields for skills, skill_years, and skill_months.
class EmployerSkillForm(forms.ModelForm):
    skill_years = forms.IntegerField(required=False)
    skill_months = forms.IntegerField(required=False)  # Ensure this is included
    
    class Meta:
        model = EmployerSkill
        fields = ['id', 'skill', 'skill_years', 'skill_months']

    # This clean method ensures that at least one of skill_years or skill_months is filled.
    def clean(self):
        cleaned_data = super().clean()
        skill_years = cleaned_data.get('skill_years', 0)
        skill_months = cleaned_data.get('skill_months', 0)

        # Validation: If both years and months are 0, raise an error
        if skill_years == 0 and skill_months == 0:
            raise forms.ValidationError("At least one of 'Skill Years' or 'Skill Months' must be filled.")

        # Make sure empty fields default to 0 instead of None
        cleaned_data['skill_years'] = skill_years if skill_years is not None else 0
        cleaned_data['skill_months'] = skill_months if skill_months is not None else 0

        return cleaned_data

# Formset for EmployerSkill, using the custom EmployerSkillForm.
EmployerSkillFormSet = modelformset_factory(EmployerSkill, form=EmployerSkillForm, extra=1)

# Custom formset class to handle row cleaning, especially when skills are left blank.
class JobFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        # Iterate through forms and remove any where the skill is blank.
        for form in self.forms:
            skill = form.cleaned_data.get('skill')
            if not skill:
                # Do not raise validation error, just remove the form data.
                form.cleaned_data = {}

    # Overriding the save method to ignore empty forms
    def save(self, commit=True):
        # Filter out any forms where the skill is blank before saving.
        self.forms = [form for form in self.forms if form.cleaned_data.get('skill')]
        return super().save(commit=commit)
