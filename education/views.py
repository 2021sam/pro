from django.shortcuts import render
from .models import Education_Model
from .forms import EducationForm

def home(request):
    education = EducationForm.objects.all()
    context = {'education':  education }
    return render(request,'education/home.html', context)   



def create_post(request):
    if request.method == 'GET':
        context = {'form': EducationForm()}
        return render(request,'education/post_form.html',context)
    elif request.method == 'POST':

        # print(HttpRequest.POST)

        form = EducationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.author = request.user
            # print(form['date_end'].value())
            date_end_str = form['date_end'].value()
            date_start_str = form['date_start'].value()
            date_end = parse_datetime(date_end_str)
            date_start = parse_datetime(date_start_str)
            duration = date_end - date_start
            user.duration = duration
            user.save()
            messages.success(request, 'The post has been created successfully.')
            return redirect('posts')
        else:
            messages.error(request, 'Please correct the following errors:')
            return render(request,'blog/post_form.html',{'form':form})  
