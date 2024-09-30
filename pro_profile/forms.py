from django import forms
from django.forms import ModelForm
from .models import Profile


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['user', 'work_authorization', 'willing_to_relocate', 'birth_month', 'birth_day', 'birth_date', 'drivers_license', 'linkedin', 'open_to_public']
        labels = {
            'work_authorization': 'Work Authorization',
            'willing_to_relocate': 'Willing to Relocate',
            'birth_date': 'Date of Birth',
            'drivers_license': 'Driver\'s License Number',
            'linkedin': 'LinkedIn Profile',
            'open_to_public': 'Open Profile to Public',
        }
        widgets = {
            'birth_date': forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}),
            'drivers_license': forms.TextInput(attrs={'placeholder': 'License Number'}),
            'linkedin': forms.TextInput(attrs={'placeholder': 'LinkedIn URL'}),
        }

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        # Make the user field non-editable by disabling it
        self.fields['user'].disabled = True
