# pro/public_market/forms.py

from django import forms
from .models import VehicleListing
from django.utils import timezone


class VehicleListingForm(forms.ModelForm):
    class Meta:
        model = VehicleListing
        fields = [
            'title',
            'description',
            'pink_slip_status',
            'year',
            'vin',
            'make',
            'model',
            'odometer',
            'condition',
            'color',
            'repairs_needed',
            'price',
            'zip_code',
            'contact_email',
            'contact_phone',
            'contact_text',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'repairs_needed': forms.Textarea(attrs={'rows': 2}),
            'contact_text': forms.CheckboxInput(),
        }
        labels = {
            'vin': 'VIN (Vehicle Identification Number)',
            'odometer': 'Odometer Reading (Miles)',
            'title_status': 'Title Status',
            'repairs_needed': 'Repairs & Costs',
        }
        help_texts = {
            'repairs_needed': 'Provide details of repairs and estimated costs.',
            'odometer': 'Enter mileage in miles.',
            'title_status': 'Select the appropriate title status for the vehicle.',
        }

    def clean_year(self):
        year = self.cleaned_data.get('year')
        current_year = timezone.now().year
        if year < 1886 or year > current_year + 1:  # The first car was built in 1886
            raise forms.ValidationError(f'Enter a valid year between 1886 and {current_year + 1}.')
        return year

    def clean_vin(self):
        vin = self.cleaned_data.get('vin')
        if vin and len(vin) != 17:
            raise forms.ValidationError('VIN must be 17 characters long.')
        return vin

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError('Price must be greater than zero.')
        return price

    def clean_zip_code(self):
        zip_code = self.cleaned_data.get('zip_code')
        if not zip_code.isdigit() or len(zip_code) not in [5, 10]:
            raise forms.ValidationError('Enter a valid ZIP code.')
        return zip_code


# pro/public_market/forms.py
# from django import forms
# from .models import VehicleListing, VehiclePhoto

# class VehiclePhotoForm(forms.ModelForm):
#     class Meta:
#         model = VehiclePhoto
#         fields = ['photo']

# VehiclePhotoFormSet = forms.modelformset_factory(
#     VehiclePhoto,
#     form=VehiclePhotoForm,
#     extra=3,  # Default number of extra image forms
# )
