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


# /Users/2021sam/apps/zyxe/pro/employer_job/views.py
# from django.shortcuts import render, get_object_or_404, redirect
# from .models import EmployerJob
# from employer_skill.models import EmployerSkill  # Assuming EmployerSkill is the correct model name
# from .forms import EmployerJobForm
# from employer_skill.forms import EmployerSkillFormSet  # Make sure this is imported



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import EmployerJob
from .forms import EmployerJobForm
from employer_skill.forms import EmployerSkillFormSet
from employer_skill.models import EmployerSkill



@login_required
def add_edit_job_with_skills(request, job_id=None):
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
        formset = EmployerSkillFormSet(request.POST)

        # Debugging output
        print(f'Form data: {request.POST}')
        print(f'Job form errors: {job_form.errors}')
        print(f'Formset errors: {formset.errors}')

        if job_form.is_valid() and formset.is_valid():
            job = job_form.save(commit=False)
            job.user = request.user
            job.save()

            skills = formset.save(commit=False)
            for skill in skills:
                skill.job = job
                skill.user = request.user
                skill.save()

            return redirect('employer_job:job-view')

        else:
            print("Job form errors:", job_form.errors)
            print("Formset errors:", formset.errors)


    max_slider_value_months = 120
    show_months = True

    return render(request, 'employer_job/add_edit_job_with_skills.html', {
        'job_form': job_form,
        'formset': formset,
        'job': job,
        'job_id': job_id,
        'max_slider_value': max_slider_value_months,
        'show_months': show_months
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
