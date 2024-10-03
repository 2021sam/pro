# /Users/2021sam/apps/zyxe/pro/employer_job/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_datetime
from django.contrib import messages
from django.http import HttpResponse
from .models import EmployerJob
from .forms import EmployerJobForm
from django.urls import path

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
def add(request):
    if request.method == 'GET':
        context = {'form': EmployerJobForm()}
        return render(request,'employer_job/add_edit.html',context)
    elif request.method == 'POST':
        form = EmployerJobForm(request.POST)
        if form.is_valid():
            i = form.save(commit=False)
            i.user = request.user
            i.save()
            messages.success(request, 'The post has been successfully created.')
            return redirect('job-view')
        else:
            messages.error(request, 'Please correct the following errors:')
            return render(request,'employer_job/add_edit.html', {'form':form})


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
