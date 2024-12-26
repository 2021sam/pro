# pro/public_market/forms.py

from django import forms
from .models import VehicleListing

class VehicleListingForm(forms.ModelForm):
    class Meta:
        model = VehicleListing
        fields = ['title', 'description', 'price', 'zip_code', 'contact_info']
