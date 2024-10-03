# /Users/2021sam/apps/zyxe/pro/employer_profile/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import  login_required
from django.http import HttpResponse
from django.contrib import messages
from .models import EmployerProfile
from .forms import EmployerProfileForm
from django.contrib.auth.models import User


#   chat suggests this version
@login_required
def profile_edit(request):
    queryset = EmployerProfile.objects.filter(user=request.user)
    print(queryset)

    profile, created = EmployerProfile.objects.get_or_create(user=request.user)
    print(f'profile: {profile}')
    print(f'created: {created}')

    if created:
        print("Profile created for the user.")
    
    if request.method == 'POST':
        form = EmployerProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('home')  # Redirect to an appropriate page after saving
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EmployerProfileForm(instance=profile)

    context = {'form': form, 'id': profile.id}
    return render(request, 'employer_profile/profile_form.html', context)




def tool_profile_mia(request):
    new_profiles = 0
    users = User.objects.all()
    for user in users:
        print(user)
        profile = EmployerProfile.objects.filter(user=user)
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
        profile = EmployerProfile.objects.filter(user=user)
        print(profile)

        if not profile:
            new_profiles += 1
            print(f'Create new profile for user: {user}')
            print(f'Create new profile: {profile}')
            profile = EmployerProfile(user=user).save()

    return HttpResponse(f'New Profiles = {new_profiles}')


def tool_profile_delete_all(request):
    profiles = EmployerProfile.objects.all()
    n = profiles.count()
    for pro in profiles:
        print(pro)
        pro.delete()

    return HttpResponse(f'Deleted {n} profiles')
