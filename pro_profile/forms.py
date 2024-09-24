from django.forms import ModelForm
from .models import Profile

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['user', 'work_authorization', 'willing_to_relocate', 'address', 'birth_month', 'birth_day', 'birth_date', 'drivers_license', 'linkedin', 'open_to_public']
