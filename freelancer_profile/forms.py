# /Users/2021sam/apps/zyxe/pro/freelancer_profile/forms.py
from django import forms
from .models import Profile

class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'date_of_birth',
        ]

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'phone_number': 'Phone Number',
            'date_of_birth': 'Date of Birth',
        }

    def clean_email(self):
        """
        Custom validation for email field, if needed.
        """
        email = self.cleaned_data.get('email')
        if not email.endswith('@example.com'):
            raise forms.ValidationError("Please use your example.com email.")
        return email









from django import forms
from .models import Profile

class EmploymentTypeForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'full_time',
            'part_time',
            'contract',
            'internship',
            'temporary',
        ]

        widgets = {
            'full_time': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'part_time': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'contract': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'internship': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'temporary': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

        labels = {
            'full_time': 'Full-time',
            'part_time': 'Part-time',
            'contract': 'Contract',
            'internship': 'Internship',
            'temporary': 'Temporary',
        }


# class EmploymentTypeForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = [
#             'full_time', 'part_time', 'self_employed', 'freelance', 'apprenticeship', 'seasonal',
#             'contract_corp_to_corp', 'contract_independent', 'contract_w2', 'contract_to_hire', 'internship'
#         ]
#         labels = {
#             'full_time': 'Full-Time',
#             'part_time': 'Part-Time',
#             'self_employed': 'Self-Employed',
#             'freelance': 'Freelance',
#             'apprenticeship': 'Apprenticeship',
#             'seasonal': 'Seasonal',
#             'contract_corp_to_corp': 'Contract Corp-to-Corp',
#             'contract_independent': 'Contract Independent',
#             'contract_w2': 'Contract W2',
#             'contract_to_hire': 'Contract-to-Hire',
#             'internship': 'Internship'
#         }








class EmploymentPreferencesForm(forms.ModelForm):
    class Meta:
        model = Profile
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

            # Location Preferences
            'location_on_site',
            'location_hybrid',
            'location_remote',

            # Travel Preference
            'travel_preference',

            # Willing to Relocate
            'willing_to_relocate',
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

            'location_on_site': forms.CheckboxInput(),
            'location_hybrid': forms.CheckboxInput(),
            'location_remote': forms.CheckboxInput(),

            'willing_to_relocate': forms.CheckboxInput(),

            # Travel preference as a number input with step increments of 10%
            'travel_preference': forms.NumberInput(attrs={
                'min': 0,
                'max': 100,
                'step': 10,
                'class': 'travel-preference-field',
                'help_text': 'Specify travel preference as a percentage in increments of 10%.'
            }),
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
            'location_on_site': 'On-Site',
            'location_hybrid': 'Hybrid',
            'location_remote': 'Remote',
            'willing_to_relocate': 'Willing to Relocate',
            'travel_preference': 'Travel Preference',
        }





class LocationPreferencesForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['location_on_site', 'location_remote', 'location_hybrid']
        labels = {
            'location_on_site': 'On-Site',
            'location_remote': 'Remote',
            'location_hybrid': 'Hybrid'
        }

class TravelRelocationForm(forms.ModelForm):
    class Meta:
        model = Profile
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
