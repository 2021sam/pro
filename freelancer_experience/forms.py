# /Users/2021sam/apps/zyxe/freelancer_experience/forms.py
from django import forms
from django.forms import modelformset_factory 
from .models import FreelancerExperience, FreelancerSkill

class FreelancerExperienceForm(forms.ModelForm):
    class Meta:
        model = FreelancerExperience
        fields = ['title', 'company', 'date_start', 'date_end', 'description']

class FreelancerSkillForm(forms.ModelForm):
    class Meta:
        model = FreelancerSkill
        fields = ['skill', 'skill_years', 'skill_months']





# from django import forms
# from django.forms import modelformset_factory, BaseInlineFormSet
# from .models import FreelancerSkill
# # from pro_experience.models import Experience


# class FreelancerSkillForm(forms.ModelForm):
#     skill_years = forms.IntegerField(required=False, initial=0)
#     skill_months = forms.IntegerField(required=False, initial=0)

#     class Meta:
#         model = FreelancerSkill
#         fields = ['skill', 'skill_years', 'skill_months']

#     def clean(self):
#         cleaned_data = super().clean()
#         skill_years = cleaned_data.get('skill_years')
#         skill_months = cleaned_data.get('skill_months')

#         # Convert None to 0 for years and months to avoid NoneType errors
#         if skill_years is None:
#             skill_years = 0
#         if skill_months is None:
#             skill_months = 0

#         # Ensure months are within the valid range of 0 to 11
#         if skill_months < 0 or skill_months > 11:
#             raise forms.ValidationError("Months must be between 0 and 11.")
        
#         # Ensure at least one field is filled (skill, year, or month)
#         if not cleaned_data.get('skill') and skill_years == 0 and skill_months == 0:
#             raise forms.ValidationError("Please provide a skill or years/months of experience.")

#         # Update the cleaned_data dict with validated values
#         cleaned_data['skill_years'] = skill_years
#         cleaned_data['skill_months'] = skill_months

#         return cleaned_data


# Formset for Skill, using the custom SkillForm
# FreelancerSkillFormSet = modelformset_factory(
#     FreelancerSkill,
#     form=FreelancerSkillForm,
#     extra=1,  # Allows for an additional form initially
#     can_delete=True  # Allow users to delete skills from the formset
# )


# class ExperienceFormSet(BaseInlineFormSet):
#     def clean(self):
#         """Override clean method to handle blank forms."""
#         super().clean()

#         forms_to_keep = []
#         for i, form in enumerate(self.forms):
#             if form.cleaned_data:
#                 skill = form.cleaned_data.get('skill')
#                 skill_years = form.cleaned_data.get('skill_years')
#                 skill_months = form.cleaned_data.get('skill_months')

#                 # Log for debugging
#                 print(f'ExperienceFormSet: clean: skill: {i}:[{skill}], Years: {skill_years}, Months: {skill_months}')

#                 # If the form is essentially empty, skip it (do not save)
#                 if not skill and skill_years == 0 and skill_months == 0:
#                     form.cleaned_data.clear()  # Clear empty form data
#                 else:
#                     forms_to_keep.append(form)

#         # Reassign only valid forms
#         self.forms = forms_to_keep

    # def save(self, commit=True):
    #     """Override save method to exclude empty forms."""
    #     print('************************   ExperienceFormSet: save')

    #     # Collect valid forms where 'skill' is filled and strip any leading/trailing whitespace
    #     valid_forms = [form for form in self.forms if form.cleaned_data.get('skill') and form.cleaned_data['skill'].strip()]

    #     print(f"Valid forms count: {len(valid_forms)}")  # Debugging output

    #     instances = []
    #     for form in valid_forms:
    #         if form.instance.pk or form.has_changed():
    #             print(f"Saving skill: {form.cleaned_data.get('skill')}, Years: {form.cleaned_data.get('skill_years')}, Months: {form.cleaned_data.get('skill_months')}")
    #             instance = form.save(commit=commit)
    #             instances.append(instance)

    #     return instances  # Return the list of saved instances
