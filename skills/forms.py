from django import forms
# from django.forms import ModelForm
from .models import Skills
from experience.models import Experience

class SkillsForm(forms.ModelForm):
    class Meta:
        model = Skills
        fields = ['skill', 'skill_years', 'skill_months']

    def __init__(self, *args, **kwargs):
            self.user = kwargs.pop('user', None)
            if self.user:
                print(self.user.id)
            super(SkillsForm, self).__init__(*args, **kwargs)
            self.fields['experience'] = forms.ModelMultipleChoiceField(queryset=Experience.objects.filter(user=self.user.id))
