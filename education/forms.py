from django.forms import ModelForm
from .models import Education_Model

class EducationForm(ModelForm):
    class Meta:
        model = Education_Model
        fields = ['school_name', 'degree_type', 'major', 'year_graduated']

    # school_name = models.CharField(max_length=30, blank=True)
    # degree_type = models.CharField(max_length=20, blank=True, choices = CHOICES_DEGREE_TYPE, default='select degree type')
    # major = models.CharField(max_length=30, blank=True)
    # year_graduated = models.SmallIntegerField(blank=True, null=True, validators=[MinValueValidator(2000), MaxValueValidator(2030)])
    # currently_enrolled = models.BooleanField()
    # gpa = models.FloatField()
    
    # skill1 = models.CharField(max_length=30, blank=True, help_text = 'Note: Skills are mutually exclusive in terms of adding time to subset skills.  Furthermore, only experience time with matching terms are added.')
    # skill1_years = models.SmallIntegerField(default=0)
    # skill1_months = models.SmallIntegerField(default=0)
    # skill2 = models.CharField(max_length=30, blank=True)
    # skill2_years = models.SmallIntegerField(default=0)
    # skill2_months = models.SmallIntegerField(default=0)
    # skill3 = models.CharField(max_length=30, blank=True)
    # skill3_years = models.SmallIntegerField(default=0)
    # skill3_months = models.SmallIntegerField(default=0)
    