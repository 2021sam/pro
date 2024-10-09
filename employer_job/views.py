# /Users/2021sam/apps/zyxe/pro/employer_job/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_datetime
from django.contrib import messages
from django.http import HttpResponse
from .models import EmployerJob
from .forms import EmployerJobForm
from django.urls import path

from employer_skill.forms import EmployerSkillForm, EmployerSkillFormSet
from django.forms import modelformset_factory
from employer_skill.models import EmployerSkill

@login_required
def home(request):
    content = {}
    return render(request, 'employer_job/home.html', content)


@login_required
def view(request):
    job = EmployerJob.objects.filter(user=request.user)
    context = {'job':  job}
    return render(request,'employer_job/view.html', context)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import EmployerJob
from .forms import EmployerJobForm
from employer_skill.forms import EmployerSkillFormSet
from employer_skill.models import EmployerSkill






# /Users/2021sam/apps/zyxe/pro/employer_job/views.py

@login_required
def add_edit_job_with_skills(request, job_id=None):
    # Fetch job if job_id is provided (edit case), otherwise create new (add case)
    if job_id:
        job = get_object_or_404(EmployerJob, pk=job_id)
        job_form = EmployerJobForm(instance=job)
        formset = EmployerSkillFormSet(queryset=EmployerSkill.objects.filter(job=job))
    else:
        job = None
        job_form = EmployerJobForm()
        formset = EmployerSkillFormSet(queryset=EmployerSkill.objects.none())

    if request.method == 'POST':
        job_form = EmployerJobForm(request.POST, instance=job)

        # Here we include request.POST when creating the formset
        formset = EmployerSkillFormSet(request.POST, queryset=EmployerSkill.objects.none() if job is None else EmployerSkill.objects.filter(job=job))
        # print(formset)
        # Validate both job form and formset
        if formset.is_valid():
            print('views.py: formset.is_valid')
        if job_form.is_valid() and formset.is_valid():
            # Save the job
            job = job_form.save(commit=False)
            job.user = request.user  # Set the current logged-in user
            job.save()

            # Save the skills, assigning the job to each skill in the formset
            skills = formset.save(commit=False)
            for skill in skills:
                if skill.skill:
                    print(f'Saving skill: [{skill.skill}], Years: {skill.skill_years}, Months: {skill.skill_months}')
                    skill.job = job  # Assign the saved job to the skill
                    skill.user = request.user  # Set the current logged-in user for each skill
                    skill.save()
                elif skill.pk is not None:  # Ensure the skill exists in the database
                    # Handle deletion
                    print(f'Delete skill: [{skill.skill}], Years: {skill.skill_years}, Months: {skill.skill_months}')
                    skill.delete()

            return redirect('employer_job:job-view')  # Adjust to your desired redirect URL
        else:
            print("Job form errors:", job_form.errors)
            print("Formset errors:", formset.errors)

    # Variable to toggle months display (can be set based on business logic)
    max_slider_value_months = 120
    show_months = True  # or False based on your logic

    return render(request, 'employer_job/add_edit_job_with_skills.html', {
        'job_form': job_form,
        'formset': formset,
        'job': job,
        'job_id': job_id,
        'max_slider_value': max_slider_value_months,  # Pass the slider max value to the template
        'show_months': show_months  # Pass the toggle variable for months
    })







@login_required
def delete(request, job_id):
    queryset = EmployerJob.objects.filter(user=request.user)
    job = get_object_or_404(queryset, pk=job_id)
    context = {'job': job}
    
    if request.method == 'GET':
        return render(request, 'employer_job/delete.html', context)
    elif request.method == 'POST':
        job.delete()
        messages.success(request,  'The post has been deleted successfully.')
        return redirect('employer_job:job-view')
