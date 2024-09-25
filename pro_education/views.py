from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_datetime
from django.contrib import messages
from django.http import HttpResponse
from .models import Education
from .forms import EducationForm


@login_required
def home(request):
    education = Education.objects.filter(user=request.user)
    # education = Education_Model.objects.all()
    context = {'education':  education }
    return render(request,'education/home.html', context)   


@login_required
def view(request):
    education = Education.objects.filter(user=request.user)
    context = {'education':  education }
    return render(request,'education/view.html', context)


@login_required
def add(request):
    if request.method == 'GET':
        context = {'form': EducationForm()}
        return render(request,'education/add_edit.html',context)
    elif request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            i = form.save(commit=False)
            i.user = request.user
            # year_graduated_str = form['year_graduated'].value()
            # i.year_graduated = parse_datetime(year_graduated_str)
            i.save()
            messages.success(request, 'The post has been successfully created.')
            return redirect('education-view')
        else:
            messages.error(request, 'Please correct the following errors:')
            return render(request,'education/add_edit.html', {'form':form})  


@login_required    
def edit(request, id):
    queryset = Education.objects.filter(user=request.user)
    education = get_object_or_404(queryset, pk=id)

    if request.method == 'GET':
        context = {'form': EducationForm(instance=education), 'id': id}
        return render(request,'education/add_edit.html', context)
    
    elif request.method == 'POST':
        form = EducationForm(request.POST, instance=education)
        if form.is_valid():
            form.save()
            messages.success(request, 'The post has been updated successfully.')
            return redirect('education-view')
        else:
            messages.error(request, 'Please correct the following errors:')
            return render(request,'education/add_edit.html', {'form':form})


@login_required
def delete(request, id):
    queryset = Education.objects.filter(user=request.user)
    education = get_object_or_404(queryset, pk=id)
    context = {'education': education}
    
    if request.method == 'GET':
        return render(request, 'education/delete.html', context)
    elif request.method == 'POST':
        education.delete()
        messages.success(request,  'The post has been deleted successfully.')
        return redirect('education-view')
