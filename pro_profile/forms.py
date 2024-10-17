from django import forms
from django.forms import ModelForm
from .models import Profile


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ['ip1', 'ip2', 'mac1', 'mac2']  # Exclude the 'user' field or any other field you don't want
        fields = [
            'user', 'work_authorization', 'willing_to_relocate', 'birth_month', 'birth_day', 
            'birth_date', 'drivers_license', 'linkedin', 'open_to_public', 'ip1', 'ip2', 'mac1', 
            'mac2', 'residential_street_address', 'residential_city_address', 
            'residential_state_address', 'residential_zip_address', 'company', 
            'company_web_site', 'work_street_address', 'work_city_address', 
            'work_state_address', 'work_zip_address', 'mobile_cell_number'
        ]
        labels = {
            'work_authorization': 'Work Authorization',
            'willing_to_relocate': 'Willing to Relocate',
            'birth_date': 'Date of Birth',
            'birth_month': 'Birth Month',
            'birth_day': 'Birth Day',
            'drivers_license': 'Driver\'s License Number',
            'linkedin': 'LinkedIn Profile',
            'open_to_public': 'Open Profile to Public',
            'ip1': 'IP Address 1',
            'ip2': 'IP Address 2',
            'mac1': 'MAC Address 1',
            'mac2': 'MAC Address 2',
            'residential_street_address': 'Residential Street Address',
            'residential_city_address': 'Residential City',
            'residential_state_address': 'Residential State',
            'residential_zip_address': 'Residential ZIP',
            'company': 'Company Name',
            'company_web_site': 'Company Website',
            'work_street_address': 'Work Street Address',
            'work_city_address': 'Work City',
            'work_state_address': 'Work State',
            'work_zip_address': 'Work ZIP',
            'mobile_cell_number': 'Mobile/Cell Number',
        }
        widgets = {
            'birth_date': forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}),
            'drivers_license': forms.TextInput(attrs={'placeholder': 'License Number'}),
            'linkedin': forms.TextInput(attrs={'placeholder': 'LinkedIn URL'}),
            'mobile_cell_number': forms.TextInput(attrs={'placeholder': '(XXX) XXX-XXXX'}),
            'residential_street_address': forms.TextInput(attrs={'placeholder': 'Street Address'}),
            'residential_city_address': forms.TextInput(attrs={'placeholder': 'City'}),
            'residential_state_address': forms.TextInput(attrs={'placeholder': 'State'}),
            'residential_zip_address': forms.TextInput(attrs={'placeholder': 'ZIP Code'}),
            'company': forms.TextInput(attrs={'placeholder': 'Company Name'}),
            'company_web_site': forms.TextInput(attrs={'placeholder': 'Company Website'}),
            'work_street_address': forms.TextInput(attrs={'placeholder': 'Street Address'}),
            'work_city_address': forms.TextInput(attrs={'placeholder': 'City'}),
            'work_state_address': forms.TextInput(attrs={'placeholder': 'State'}),
            'work_zip_address': forms.TextInput(attrs={'placeholder': 'ZIP Code'}),
        }

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        # Make the user field non-editable by disabling it
        self.fields['user'].disabled = True




from django import forms
from .models import Profile

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
