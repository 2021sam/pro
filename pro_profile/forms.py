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
