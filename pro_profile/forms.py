from django import forms
from django.forms import ModelForm
from .models import Profile


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['user', 'work_authorization', 'willing_to_relocate', 'birth_month', 'birth_day', 'birth_date', 'drivers_license', 'linkedin', 'open_to_public']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        # Make the user field non-editable by disabling it
        self.fields['user'].disabled = True
