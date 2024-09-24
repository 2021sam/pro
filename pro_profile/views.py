from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import  login_required
from django.http import HttpResponse
from django.contrib import messages
from .models import Profile
from .forms import ProfileForm
from django.contrib.auth.models import User


# @login_required
# def profile_edit(request):
#     profile, created = Profile.objects.get_or_create(user=request.user)

#     if created:
#         print("Profile created for the user.")
    
#     form = ProfileForm(instance=profile)
#     queryset = Profile.objects.filter(user=request.user)
#     print(queryset)
#     for e in queryset:
#         print(e.id)
#         print(e.user)
#         id = e.id
#         current_user = e.user
#         print(f'id = {id}')
#         print(f'user={current_user}')

#     form = get_object_or_404(queryset, pk=id)

#     if request.method == 'GET':
#         context = {'form': ProfileForm(instance=form), 'id': id}
#         return render(request,'pro_profile/profile_form.html',context)

#     elif request.method == 'POST':
#         form = ProfileForm(request.POST, instance=form)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'The post has been updated successfully.')
#             return redirect('home')
#         else:
#             messages.error(request, 'Please correct the following errors:')
#             return render(request,'pro_profile/profile_form.html',{'form':form})



#   chat suggests this version
@login_required
def profile_edit(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if created:
        print("Profile created for the user.")
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('home')  # Redirect to an appropriate page after saving
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileForm(instance=profile)

    context = {'form': form, 'id': profile.id}
    return render(request, 'pro_profile/profile_form.html', context)




def tool_profile_mia(request):
    new_profiles = 0
    users = User.objects.all()
    for user in users:
        print(user)
        profile = Profile.objects.filter(user=user)
        print(profile)
        if not profile:
            new_profiles += 1
            print(f'Profile MIA for user: {user}')
    return HttpResponse(f'Profiles MIA = {new_profiles}')


def tool_profile_create_all(request):
    new_profiles = 0
    users = User.objects.all()
    for user in users:
        print(user)
        profile = Profile.objects.filter(user=user)
        print(profile)

        if not profile:
            new_profiles += 1
            print(f'Create new profile for user: {user}')
            print(f'Create new profile: {profile}')
            profile = Profile(user=user).save()

    return HttpResponse(f'New Profiles = {new_profiles}')


def tool_profile_delete_all(request):
    profiles = Profile.objects.all()
    n = profiles.count()
    for pro in profiles:
        print(pro)
        pro.delete()

    return HttpResponse(f'Deleted {n} profiles')
