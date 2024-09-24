from django import forms
from django.forms import ModelForm
from .models import Profile

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['user', 'work_authorization', 'willing_to_relocate', 'address', 'birth_month', 'birth_day', 'birth_date', 'drivers_license', 'linkedin', 'open_to_public']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget.attrs['readonly'] = True  # Make user field read-only







# from django import forms
# from .models import Profile
# from django.contrib.auth import get_user_model

# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['address', 'birth_date', 'mobile_number', 'mobile_carrier']  # Add other editable fields

#     def __init__(self, *args, **kwargs):
#         super(ProfileForm, self).__init__(*args, **kwargs)
#         self.fields['user'].widget.attrs['readonly'] = True



# from django import forms
# from django.forms import ModelForm
# from .models import Profile

# class ProfileForm(ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['user', 'work_authorization', 'willing_to_relocate', 'address', 'birth_month', 'birth_day', 'birth_date', 'drivers_license', 'linkedin', 'open_to_public']

        # widgets = {
        #     'user': forms.EmailInput(attrs={'readonly': 'readonly'}),
        # }
