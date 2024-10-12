# /Users/2021sam/apps/zyxe/pro/pro_experience/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Experience
from .forms import ExperienceForm
from pro_skills.forms import SkillFormSet
from pro_skills.models import Skill

@login_required
def home(request):
    content = {}
    return render(request, 'pro_experience/home.html', content)

@login_required
def view(request):
    experience_list = Experience.objects.filter(user=request.user)
    context = {'experience_list': experience_list}
    return render(request, 'pro_experience/experience_list.html', context)

@login_required
def add_edit_experience(request, experience_id=None):
    # Fetch experience if experience_id is provided (edit case), otherwise create new (add case)
    if experience_id:
        experience = get_object_or_404(Experience, pk=experience_id)
        experience_form = ExperienceForm(instance=experience)
        formset = SkillFormSet(queryset=Skill.objects.filter(experience=experience))
    else:
        experience = None
        experience_form = ExperienceForm()
        formset = SkillFormSet(queryset=Skill.objects.none())

    if request.method == 'POST':
        experience_form = ExperienceForm(request.POST, instance=experience)
        formset = SkillFormSet(request.POST, queryset=Skill.objects.filter(experience=experience) if experience else Skill.objects.none())

        if experience_form.is_valid() and formset.is_valid():
            # Save the experience
            experience = experience_form.save(commit=False)
            experience.user = request.user  # Set the current logged-in user
            experience.save()

            # Save the skills associated with the experience
            skills = formset.save(commit=False)
            for skill in skills:
                skill.experience = experience
                skill.user = request.user
                skill.save()

            # Handle deletions if any
            for obj in formset.deleted_objects:
                obj.delete()

            formset.save()  # Ensure formset is saved

            return redirect('pro_experience:pro-experience-list')

    return render(request, 'pro_experience/experience_form.html', {
        'experience_form': experience_form,
        'formset': formset,
        'experience': experience,
        'experience_id': experience_id
    })

@login_required
def delete(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
    if request.method == 'POST':
        experience.delete()
        return redirect('pro_experience:pro-experience-list')
    return render(request, 'pro_experience/experience_confirm_delete.html', {'experience': experience})
