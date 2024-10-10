# /Users/2021sam/apps/zyxe/pro/employer_skill/forms.py
from django import forms
from django.forms import modelformset_factory, BaseInlineFormSet, BaseFormSet
from .models import EmployerSkill
from employer_job.models import EmployerJob

# EmployerSkillForm handles the fields for skills, skill_years, and skill_months.
class EmployerSkillForm(forms.ModelForm):
    skill_years = forms.IntegerField(required=False, initial=0)
    skill_months = forms.IntegerField(required=False, initial=0)

    class Meta:
        model = EmployerSkill
        fields = ['skill', 'skill_years', 'skill_months']

    def clean(self):
        cleaned_data = super().clean()
        skill_years = cleaned_data.get('skill_years', 0)
        skill_months = cleaned_data.get('skill_months', 0)

        if skill_months < 0 or skill_months > 11:
            raise forms.ValidationError("Months must be between 0 and 11.")

        return cleaned_data


# Formset for EmployerSkill, using the custom EmployerSkillForm.
EmployerSkillFormSet = modelformset_factory(EmployerSkill, form=EmployerSkillForm, extra=1, can_delete=True)

# class JobFormSet(BaseFormSet):
class JobFormSet(BaseInlineFormSet):
    def clean(self):
        """Override clean method to handle blank forms."""
        super().clean()

        for i, form in enumerate(self.forms):
            skill = form.cleaned_data.get('skill')
            print(f'JobFormSet: clean: skill: {i}:[{skill}]')


    def save(self, commit=True):
        print('************************   JobFormSet: save')
        """Override save method to exclude empty forms."""
        # Collect valid forms where 'skill' is filled
        valid_forms = [form for form in self.forms if form.cleaned_data.get('skill') and form.cleaned_data['skill'].strip()]

        print(f"Valid forms count: {len(valid_forms)}")  # Debugging output

        instances = []
        for form in valid_forms:
            if form.instance.pk or form.has_changed():
                print(f"Saving skill: {form.cleaned_data.get('skill')}, Years: {form.cleaned_data.get('skill_years')}, Months: {form.cleaned_data.get('skill_months')}")
                instance = form.save(commit=commit)
                instances.append(instance)

        return instances  # Return the list of saved instances
