# /Users/2021sam/apps/zyxe/pro/employer_skill/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import EmployerSkill
from .forms import EmployerSkillForm, EmployerSkillFormSet
from django.forms import modelformset_factory


def skill_list(request):
    skills = EmployerSkill.objects.all()
    return render(request, 'employer_skill/skill_list.html', {'skills': skills})

# def skill_add(request):
#     # Use modelformset_factory to create a formset for Skill model
#     SkillFormSet = modelformset_factory(EmployerSkill, form=EmployerSkillForm, extra=1)
#     if request.method == 'POST':
#         formset = SkillFormSet(request.POST)
#         if formset.is_valid():
#             instances = formset.save(commit=False)
#             for instance in instances:
#                 instance.user = request.user
#                 instance.save()
#             formset.save_m2m()  # Save many-to-many relationships if needed
#             return redirect('employer_skill:emp_skill_list')
#         else:
#             print('Formset Errors:', formset.errors)
#     else:
#         formset = SkillFormSet(queryset=EmployerSkill.objects.none())  # Show empty formset for new entries

#     # Render the formset in the template for creating multiple skills
#     return render(request, 'employer_skill/skill_formset.html', {'formset': formset, 'form_type': 'create'})

from employer_job.models import EmployerJob

def skill_add(request, job_id=None):
    # Ensure a job is selected first; if no job_id, redirect to job selection/creation page
    if not job_id:
        return redirect('employer_skill:job_add')

    # Get the selected job
    selected_job = get_object_or_404(EmployerJob, id=job_id)

    # Use modelformset_factory to create a formset for Skill model
    SkillFormSet = modelformset_factory(EmployerSkill, form=EmployerSkillForm, extra=1)

    if request.method == 'POST':
        formset = SkillFormSet(request.POST)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.user = request.user
                instance.job = selected_job  # Lock job to the selected one
                instance.save()
            formset.save_m2m()
            return redirect('employer_skill:emp_skill_list')
        else:
            print('Formset Errors:', formset.errors)
    else:
        formset = SkillFormSet(queryset=EmployerSkill.objects.none())  # Show empty formset for new entries

    # Render the formset in the template and pass the selected job
    return render(request, 'employer_skill/skill_formset.html', {'formset': formset, 'job': selected_job, 'form_type': 'create'})




def skill_edit(request, pk):
    skill = get_object_or_404(EmployerSkill, pk=pk)
    if request.method == 'POST':
        form = EmployerSkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            return redirect('employer_skill:emp_skill_list')
    else:
        form = EmployerSkillForm(instance=skill)

    # Render the single form in the template for editing an existing skill
    return render(request, 'employer_skill/skill_form.html', {'form': form, 'form_type': 'edit'})

def skill_delete(request, pk):
    skill = get_object_or_404(EmployerSkill, pk=pk)
    if request.method == 'POST':
        skill.delete()
        return redirect('employer_skill:emp_skill_list')
    return render(request, 'employer_skill/skill_confirm_delete.html', {'skill': skill})
