from django.forms import ModelForm
from .models import Education_Model

class EducationForm(ModelForm):
    class Meta:
        model = Education_Model
        fields = ['school_name', 'degree_type', 'major', 'gpa', 'currently_enrolled', 'year_graduated']
