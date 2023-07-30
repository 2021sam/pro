from django.shortcuts import render, redirect
from .models import Education_Model
from .forms import EducationForm
from django.utils.dateparse import parse_datetime
from django.contrib import messages
from django.http import HttpResponse


def home(request):
    # return HttpResponse('Education')
    education = Education_Model.objects.all()
    context = {'education':  education }
    return render(request,'education/home.html', context)   

def add(request):
    if request.method == 'GET':
        context = {'form': EducationForm()}
        return render(request,'education/form.html',context)
    elif request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            i = form.save(commit=False)
            i.author = request.user
            # print(form['date_end'].value())
            date_end_str = form['date_end'].value()
            date_start_str = form['date_start'].value()
            date_end = parse_datetime(date_end_str)
            date_start = parse_datetime(date_start_str)
            duration = date_end - date_start
            i.duration = duration
            i.save()
            messages.success(request, 'The post has been created successfully.')
            return redirect('posts')
        else:
            messages.error(request, 'Please correct the following errors:')
            return render(request,'blog/post_form.html', {'form':form})  
