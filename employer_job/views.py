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

@login_required
def add_or_edit_job_with_skills(request, id=None):
    # Handle job editing if ID is provided, else handle adding a new job
    if id:
        job = get_object_or_404(EmployerJob, pk=id, user=request.user)
    else:
        job = None

    if request.method == 'POST':
        job_form = EmployerJobForm(request.POST, instance=job)
        SkillFormSet = modelformset_factory(EmployerSkill, form=EmployerSkillForm, extra=1)
        formset = SkillFormSet(request.POST)
        
        if job_form.is_valid() and formset.is_valid():
            job = job_form.save(commit=False)
            job.user = request.user
            job.save()

            instances = formset.save(commit=False)
            for instance in instances:
                instance.job = job  # Associate the skills with the job
                instance.user = request.user
                instance.save()

            messages.success(request, 'Job and skills have been saved successfully.')
            return redirect('employer_job:job-view')
    
    else:
        job_form = EmployerJobForm(instance=job)
        SkillFormSet = modelformset_factory(EmployerSkill, form=EmployerSkillForm, extra=1)
        formset = SkillFormSet(queryset=EmployerSkill.objects.filter(job=job))

    return render(request, 'employer_job/add_edit_job_with_skills.html', {
        'job_form': job_form,
        'formset': formset,
        'job': job,
    })




















# @login_required
# def add(request):
#     if request.method == 'GET':
#         context = {'form': EmployerJobForm()}
#         return render(request,'employer_job/add_edit.html',context)
#     elif request.method == 'POST':
#         form = EmployerJobForm(request.POST)
#         if form.is_valid():
#             i = form.save(commit=False)
#             i.user = request.user
#             i.save()
#             messages.success(request, 'The post has been successfully created.')
#             return redirect('job-view')
#         else:
#             messages.error(request, 'Please correct the following errors:')
#             return render(request,'employer_job/add_edit.html', {'form':form})

def add(request):
    # Create or select a job first before adding skills
    if request.method == 'POST':
        form = EmployerJobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.user = request.user
            job.save()
            return redirect('employer_skill:skill_add', job_id=job.id)
    else:
        form = EmployerJobForm()

    return render(request, 'employer_job/add.html', {'form': form})





@login_required    
def edit(request, id):
    queryset = EmployerJob.objects.filter(user=request.user)
    job = get_object_or_404(queryset, pk=id)

    if request.method == 'GET':
        context = {'form': EmployerJobForm(instance=job), 'id': id}
        return render(request,'employer_job/add_edit.html', context)
    
    elif request.method == 'POST':
        form = EmployerJobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'The post has been updated successfully.')
            return redirect('employer_job:job-view')
        else:
            messages.error(request, 'Please correct the following errors:')
            return render(request,'employer_job/add_edit.html', {'form':form})


@login_required
def delete(request, id):
    queryset = EmployerJob.objects.filter(user=request.user)
    job = get_object_or_404(queryset, pk=id)
    context = {'job': job}
    
    if request.method == 'GET':
        return render(request, 'employer_job/delete.html', context)
    elif request.method == 'POST':
        job.delete()
        messages.success(request,  'The post has been deleted successfully.')
        return redirect('employer_job:job-view')
