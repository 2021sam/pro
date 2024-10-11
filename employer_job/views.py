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
    return render(request,'employer_job/job_list.html', context)


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
        formset = EmployerSkillFormSet(request.POST, queryset=EmployerSkill.objects.filter(job=job) if job else EmployerSkill.objects.none())

        # Validate both job form and formset
        if job_form.is_valid() and formset.is_valid():
            print('views.py: formset.is_valid')

            # Save the job
            job = job_form.save(commit=False)
            job.user = request.user  # Set the current logged-in user
            job.save()

            # Save the skills and handle deletions automatically
            skills = formset.save(commit=False)  # Get the forms to save
            for skill in skills:
                skill.job = job  # Assign the saved job to each skill
                skill.user = request.user  # Set the current logged-in user for each skill
                skill.save()

            # Handle deletions manually if using commit=False
            for obj in formset.deleted_objects:
                print(f'Deleting skill: {obj.skill}, Years: {obj.skill_years}, Months: {obj.skill_months}')
                obj.delete()

            # Save the formset to ensure deletions are handled
            formset.save()

            return redirect('employer_job:job-view')  # Adjust to your desired redirect URL
        else:
            print("Job form errors:", job_form.errors)
            print("Formset errors:", formset.errors)

    return render(request, 'employer_job/job_form.html', {
        'job_form': job_form,
        'formset': formset,
        'job': job,
        'job_id': job_id
    })


@login_required
def delete(request, job_id):
    queryset = EmployerJob.objects.filter(user=request.user)
    job = get_object_or_404(queryset, pk=job_id)
    context = {'job': job}
    
    if request.method == 'GET':
        return render(request, 'employer_job/job_delete_confirmation.html', context)
    elif request.method == 'POST':
        job.delete()
        messages.success(request,  'The post has been deleted successfully.')
        return redirect('employer_job:job-view')
