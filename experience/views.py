from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_datetime
from django.contrib import messages
from django.http import HttpResponse
from .models import Experience
from .forms import ExperienceForm


@login_required
def home(request):
    experience = Experience.objects.filter(author=request.user)
    context = {'experience':  experience }
    return render(request,'experience/home.html', context)

@login_required
def add(request):
    if request.method == 'GET':
        context = {'form': ExperienceForm()}
        return render(request,'experience/form.html',context)
    elif request.method == 'POST':
        form = ExperienceForm(request.POST)
        if form.is_valid():
            i = form.save(commit=False)
            i.author = request.user
            i.save()
            messages.success(request, 'The post has been successfully created.')
            return redirect('experience-view')
        else:
            messages.error(request, 'Please correct the following errors:')
            return render(request,'experience/form.html', {'form':form})  



@login_required
def delete_experience(request, id):
    queryset = Experience.objects.filter(author=request.user)
    experience = get_object_or_404(queryset, pk=id)
    context = {'experience': experience}
    
    if request.method == 'GET':
        return render(request, 'experience/delete.html', context)
    elif request.method == 'POST':
        experience.delete()
        messages.success(request,  'The post has been deleted successfully.')
        return redirect('experience-view')

@login_required    
def edit_experience(request, id):
    queryset = Experience.objects.filter(author=request.user)
    experience = get_object_or_404(queryset, pk=id)

    if request.method == 'GET':
        context = {'form': ExperienceForm(instance=experience), 'id': id}
        return render(request,'experience/form.html', context)
    
    elif request.method == 'POST':
        form = ExperienceForm(request.POST, instance=experience)
        if form.is_valid():
            form.save()
            messages.success(request, 'The post has been updated successfully.')
            return redirect('experience-view')
        else:
            messages.error(request, 'Please correct the following errors:')
            return render(request,'experience/form.html', {'form':form})
