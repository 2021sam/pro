# /Users/2021sam/apps/zyxe/freelancer_experience/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import FreelancerExperience, FreelancerSkill
from .forms import FreelancerExperienceForm, FreelancerSkillForm
from django.forms import modelformset_factory

@login_required
def add_experience(request):
    ExperienceFormSet = modelformset_factory(FreelancerSkill, form=FreelancerSkillForm, extra=1)

    if request.method == 'POST':
        experience_form = FreelancerExperienceForm(request.POST)
        formset = ExperienceFormSet(request.POST, queryset=FreelancerSkill.objects.none())

        if experience_form.is_valid() and formset.is_valid():
            experience = experience_form.save(commit=False)
            experience.profile = request.user.freelancerprofile
            experience.save()

            skills = formset.save(commit=False)
            for skill in skills:
                skill.experience = experience
                skill.save()

            return redirect('freelancer_experience:experience-list')
    else:
        experience_form = FreelancerExperienceForm()
        formset = ExperienceFormSet(queryset=FreelancerSkill.objects.none())

    return render(request, 'freelancer_experience/add_experience.html', {
        'experience_form': experience_form,
        'formset': formset,
    })
