from django import forms

class FreelancerSearchForm(forms.Form):
    recruiter_zip_code = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Job Zip Code'})
    )
    commute_limit_miles = forms.IntegerField(
        initial=50,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Commute Limit in Miles'}),
        help_text="Enter the maximum commute distance in miles."
    )

    def clean_recruiter_zip_code(self):
        """
        Add validation for recruiter zip code, e.g., ensuring it's a valid format or length.
        """
        zip_code = self.cleaned_data.get('recruiter_zip_code')
        if len(zip_code) != 5 or not zip_code.isdigit():
            raise forms.ValidationError("Please enter a valid 5-digit zip code.")
        return zip_code
