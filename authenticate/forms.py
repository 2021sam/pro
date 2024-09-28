# C:\Users\2021sam\apps\zyxe\pro\authenticate\forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

CARRIER_CHOICES = [
    ('att', 'AT&T'),
    ('verizon', 'Verizon'),
    ('tmobile', 'T-Mobile'),
    ('sprint', 'Sprint'),
    # Add more carriers as needed
]


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)

        # Set username to be the email
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        user.is_active = False  # Deactivate account until email verification

        if commit:
            user.save()
        return user



from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        # Do not raise ValidationError here for inactive users
        # Let the view handle it
        pass


from django import forms
from .models import CustomUser

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'mobile_number', 'mobile_carrier', 'mobile_authenticated']

        widgets = {
            'email': forms.EmailInput(attrs={'readonly': 'readonly'}),
            'mobile_authenticated': forms.CheckboxInput(attrs={'disabled': 'disabled'}),
        }


    def clean_mobile_number(self):
        mobile_number = self.cleaned_data.get('mobile_number')
        if not mobile_number:
            raise forms.ValidationError("Mobile number is required for enabling 2FA.")
        return mobile_number


from django import forms

class TwoFactorForm(forms.Form):
    code = forms.CharField(max_length=6, label='Enter 2FA Code')