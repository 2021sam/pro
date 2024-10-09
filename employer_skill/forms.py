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
    print('employer_skill: forms.py: JobFormSet')

    def clean(self):
        """Override clean method to handle blank forms."""
        super().clean()

        forms_to_keep = []
        for form in self.forms:
            if form.is_valid():  # Ensure the form is valid
                skill = form.cleaned_data.get('skill', None)
                print(f'********************* skill: [{skill}]')
                # Only keep forms with non-empty skill
                if skill and skill.strip():  # Check if skill is not empty or just whitespace
                    forms_to_keep.append(form)
                else:
                    # If skill is blank, remove it from cleaned_data to avoid saving
                    print(f"Excluding form with empty skill.")
                    form.cleaned_data.clear()
            else:
                print(f"Invalid form detected: {form.errors}")
        
        # Reassign the valid forms to the formset
        self.forms = forms_to_keep

    def save(self, commit=True):
        """Override save method to exclude empty forms."""
        # Collect forms where 'skill' is filled
        valid_forms = [form for form in self.forms if form.cleaned_data.get('skill')]

        print(f"Valid forms count: {len(valid_forms)}")

        # Use the parent class's save method, but only for valid forms
        instances = []
        for form in valid_forms:
            if form.instance.pk or form.has_changed():
                instance = form.save(commit=commit)
                instances.append(instance)

        return instances  # Return the list of saved instances
