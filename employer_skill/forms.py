from django import forms
from django.forms import modelformset_factory, BaseInlineFormSet
from .models import EmployerSkill
from employer_job.models import EmployerJob

# EmployerSkillForm handles the fields for skills, skill_years, and skill_months.
class EmployerSkillForm(forms.ModelForm):
    skill = forms.CharField(required=False)  # Make skill optional
    skill_years = forms.IntegerField(required=False, initial=0)
    skill_months = forms.IntegerField(required=False, initial=0)

    class Meta:
        model = EmployerSkill
        fields = ['id', 'skill', 'skill_years', 'skill_months']

    def clean(self):
        print('EmployerSkillForm: clean')
        cleaned_data = super().clean()
        skill_years = cleaned_data.get('skill_years', 0)
        skill_months = cleaned_data.get('skill_months', 0)

        # Ensure at least one of skill_years or skill_months is filled
        if skill_years == 0 and skill_months == 0:
            raise forms.ValidationError("At least one of 'Skill Years' or 'Skill Months' must be filled.")

        # Make sure empty fields default to 0 instead of None
        cleaned_data['skill_years'] = skill_years if skill_years is not None else 0
        cleaned_data['skill_months'] = skill_months if skill_months is not None else 0

        return cleaned_data

# Formset for EmployerSkill, using the custom EmployerSkillForm.
EmployerSkillFormSet = modelformset_factory(EmployerSkill, form=EmployerSkillForm, extra=1)

class JobFormSet(BaseInlineFormSet):
    def clean(self):
        """Override clean method to handle blank forms."""
        super().clean()

        forms_to_keep = []
        for form in self.forms:
            if form.is_valid():  # Check if the form is valid
                skill = form.cleaned_data.get('skill', None)
                print(f'********************* skill: [{skill}]')  # Debugging output

                # Only keep forms where skill is not blank or just whitespace
                if skill and skill.strip():
                    forms_to_keep.append(form)
                else:
                    # Log and clear forms with empty skill
                    print(f"Excluding form with empty skill: {skill}")
                    form.cleaned_data.clear()  # Clear cleaned_data to avoid saving
            else:
                print(f"Form errors: {form.errors}")  # Log any form errors

        # Reassign only the valid forms (with non-blank skill) to the formset
        self.forms = forms_to_keep

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
