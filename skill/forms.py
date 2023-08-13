from django import forms
# from django.forms import ModelForm
from .models import Skill
from experience.models import Experience
from django.forms import BaseModelFormSet

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['experience', 'skill', 'skill_years', 'skill_months']


    def __init__(self, *args, **kwargs):
            self.user = kwargs.pop('user', None)
            if self.user:
                print('SkillForm __init__:')
                print(self.user.id)
                super(SkillForm, self).__init__(*args, **kwargs)
                mystyle = {"style": "width:300px;", "size": 1, "rows": 10} # rows does not seem to have an affect
                self.fields['experience'] = forms.ModelChoiceField(queryset=Experience.objects.filter(user=self.user.id), widget=forms.Select(), required=False)
                self.fields["experience"].widget.attrs = mystyle
                self.fields["skill"].widget.attrs = {"style": "width:300px;"}

# class BaseSkillFormSet(BaseModelFormSet):
#      def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         #   self.queryset = Skill.objects.all()
#         # self.queryset = Skill.objects.filter(user=self.user)
