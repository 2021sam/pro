# /Users/2021sam/apps/zyxe/pro/employer_skill/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import EmployerSkill
from .forms import EmployerSkillForm, EmployerSkillFormSet
from django.forms import modelformset_factory


def skill_list(request):
    skills = EmployerSkill.objects.all()
    return render(request, 'employer_skill/skill_list.html', {'skills': skills})



from django.shortcuts import render, redirect, get_object_or_404
from .models import EmployerSkill
from .forms import EmployerSkillForm, EmployerSkillFormSet
from django.forms import modelformset_factory
from employer_job.models import EmployerJob

def skill_add(request, job_id):
    # Get the job based on the job_id from the URL
    job = get_object_or_404(EmployerJob, id=job_id)
    print(f'job_id: {job_id}')
    print(f'job: {job}')
    # Use modelformset_factory to create a formset for the EmployerSkill model
    SkillFormSet = modelformset_factory(EmployerSkill, form=EmployerSkillForm, extra=1)

    if request.method == 'POST':
        formset = SkillFormSet(request.POST)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.user = request.user  # Assign the current user
                instance.job = job  # Assign the job from the URL
                instance.save()
            formset.save_m2m()  # Save any many-to-many relationships, if any
            return redirect('employer_skill:emp_skill_list')
        else:
            print('Formset Errors:', formset.errors)
    else:
        # Ensure to set the job for each form in the formset
        # formset = SkillFormSet(queryset=EmployerSkill.objects.filter(job=job))
        formset = SkillFormSet(queryset=EmployerSkill.objects.none())  # Show an empty formset for new entries

    # Render the formset in the template for creating multiple skills, with the job already set
    return render(request, 'employer_skill/skill_formset.html', {'formset': formset, 'job': job, 'form_type': 'create'})






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

# from django.shortcuts import render, redirect, get_object_or_404
# from .models import EmployerSkill
# from .forms import EmployerSkillForm, EmployerSkillFormSet
# from employer_job.models import EmployerJob
# from django.forms import modelformset_factory


# def skill_add(request, job_id):
#     # Get the job based on the job_id from the URL
#     job = get_object_or_404(EmployerJob, id=job_id)

#     # Use modelformset_factory to create a formset for the EmployerSkill model
#     SkillFormSet = modelformset_factory(EmployerSkill, form=EmployerSkillForm, extra=1)

#     if request.method == 'POST':
#         formset = SkillFormSet(request.POST)
#         if formset.is_valid():
#             instances = formset.save(commit=False)
#             for instance in instances:
#                 instance.user = request.user  # Assign the current user
#                 instance.job = job  # Assign the job passed in the URL
#                 instance.save()
#             formset.save_m2m()  # Save any many-to-many relationships, if any
#             return redirect('employer_skill:emp_skill_list')
#         else:
#             print('Formset Errors:', formset.errors)
#     else:
#         formset = SkillFormSet(queryset=EmployerSkill.objects.none())  # Show an empty formset for new entries

#     # Render the formset in the template for creating multiple skills, with the job already set
#     return render(request, 'employer_skill/skill_formset.html', {'formset': formset, 'job': job, 'form_type': 'create'})




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
