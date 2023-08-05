from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import  login_required
from django.http import HttpResponse
from django.contrib import messages
from .models import Profile
from .forms import ProfileForm


# Create your views here.
# http://localhost:8000/profile/edit/1
# def profile_edit(request, id):

@login_required
def profile_edit(request):
    queryset = Profile.objects.filter(user=request.user)
    print(queryset)
    for e in queryset:
        print(e.id)
        print(e.user)
        id = e.id
        current_user = e.user
        print(f'id = {id}')
        print(f'user={current_user}')
   
    form = get_object_or_404(queryset, pk=id)

    if request.method == 'GET':
        context = {'form': ProfileForm(instance=form), 'id': id}
        return render(request,'streetcred/profile_form.html',context)

    elif request.method == 'POST':
        form = ProfileForm(request.POST, instance=form)
        if form.is_valid():
            form.save()
            messages.success(request, 'The post has been updated successfully.')
            return redirect('posts')
        else:
            messages.error(request, 'Please correct the following errors:')
            return render(request,'streetcred/profile_form.html',{'form':form})