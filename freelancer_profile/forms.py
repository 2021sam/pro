# /Users/2021sam/apps/zyxe/pro/freelancer_profile/forms.py
from django import forms
from .models import FreelancerProfile

class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = FreelancerProfile
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'date_of_birth',
            'residential_street',
            'residential_city',
            'residential_state',
            'residential_zip_code',
            'work_authorization',  # Add this field
            'open_to_public',      # Add this field
        ]

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'residential_street': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street'}),
            'residential_city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'residential_state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'residential_zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zip'}),
            'work_authorization': forms.Select(attrs={'class': 'form-control'}),  # Dropdown for work authorization
            'open_to_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),  # Checkbox for public access
        }

        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'phone_number': 'Phone Number',
            'date_of_birth': 'Date of Birth',
            'work_authorization': 'Work Authorization',  # Label for work authorization
            'open_to_public': 'Open to Public',          # Label for public access checkbox
        }


    def clean_email(self):
        """
        Custom validation for email field, if needed.
        """
        email = self.cleaned_data.get('email')
        # if not email.endswith('@example.com'):
        #     raise forms.ValidationError("Please use your example.com email.")
        return email


class EmploymentPreferencesForm(forms.ModelForm):
    class Meta:
        model = FreelancerProfile
        fields = [
            # Employment Type Preferences
            'full_time',
            'part_time',
            'self_employed',
            'freelance',
            'apprenticeship',
            'seasonal',
            'contract_corp_to_corp',
            'contract_independent',
            'contract_w2',
            'contract_to_hire',
            'internship',
            'temporary',
            'permanent',
            'contract',
        ]
        widgets = {
            # Checkbox widgets for boolean fields
            'full_time': forms.CheckboxInput(),
            'part_time': forms.CheckboxInput(),
            'self_employed': forms.CheckboxInput(),
            'freelance': forms.CheckboxInput(),
            'apprenticeship': forms.CheckboxInput(),
            'seasonal': forms.CheckboxInput(),
            'contract_corp_to_corp': forms.CheckboxInput(),
            'contract_independent': forms.CheckboxInput(),
            'contract_w2': forms.CheckboxInput(),
            'contract_to_hire': forms.CheckboxInput(),
            'internship': forms.CheckboxInput(),
            'temporary': forms.CheckboxInput(),
            'permanent': forms.CheckboxInput(),
            'contract': forms.CheckboxInput(),
        }
        labels = {
            'full_time': 'Full-Time',
            'part_time': 'Part-Time',
            'self_employed': 'Self-Employed',
            'freelance': 'Freelance',
            'apprenticeship': 'Apprenticeship',
            'seasonal': 'Seasonal',
            'contract_corp_to_corp': 'Contract Corp-to-Corp',
            'contract_independent': 'Contract Independent',
            'contract_w2': 'Contract W2',
            'contract_to_hire': 'Contract-to-Hire',
            'internship': 'Internship',
            'temporary': 'Temporary',
            'permanent': 'Permanent',
            'contract': 'Contract',
        }


class LocationPreferencesForm(forms.ModelForm):
    class Meta:
        model = FreelancerProfile
        fields = ['location_on_site', 'location_remote', 'location_hybrid', 'commute_limit_miles', 'commute_limit_minutes']
        labels = {
            'location_on_site': 'On-Site',
            'location_remote': 'Remote',
            'location_hybrid': 'Hybrid'
        }

class TravelRelocationForm(forms.ModelForm):
    class Meta:
        model = FreelancerProfile
        fields = ['travel_preference', 'willing_to_relocate']
        widgets = {
            'travel_preference': forms.NumberInput(attrs={'min': 0, 'max': 100, 'step': 10}),
        }
        help_texts = {
            'travel_preference': 'Specify travel preference as a percentage (in increments of 10%).',
        }
        labels = {
            'travel_preference': 'Travel Preference (%)',
            'willing_to_relocate': 'Willing to Relocate'
        }


class DesiredTitleForm(forms.ModelForm):
    class Meta:
        model = FreelancerProfile
        fields = [
            'desired_job_title',
            'desired_salary',
            'desired_hourly_rate'
            ]
