from django import forms
# from django.forms import ModelForm
from .models import Skill
from experience.models import Experience
from django.forms import BaseModelFormSet

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['skill', 'skill_years', 'skill_months']

    def __init__(self, *args, **kwargs):
            self.user = kwargs.pop('user', None)
            if self.user:
                print(self.user.id)
            super(SkillForm, self).__init__(*args, **kwargs)
            self.fields['experience'] = forms.ModelMultipleChoiceField(queryset=Experience.objects.filter(user=self.user.id))



# class BaseSkillFormSet(BaseModelFormSet):
#      def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         #   self.queryset = Skill.objects.all()
#         # self.queryset = Skill.objects.filter(user=self.user)
