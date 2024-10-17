# /Users/2021sam/apps/zyxe/pro/freelancer_profile/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError

from .models import Profile
from .forms import PersonalInfoForm, EmploymentTypeForm, LocationPreferencesForm, TravelRelocationForm


@method_decorator(login_required, name='dispatch')  # Ensure all methods require login
class ProfileMultiStepFormView(View):
    form_list = [
        PersonalInfoForm,
        EmploymentTypeForm,
        LocationPreferencesForm,
        TravelRelocationForm
    ]  # List of forms for each step
    step_titles = ["Personal Information", "Employment Preferences", "Location Preferences", "Travel & Relocation"]  # Titles for each step
    template_list = [
        'freelancer_profile/personal_info_form.html',
        'freelancer_profile/employment_type_form.html',
        'freelancer_profile/location_preferences_form.html',
        'freelancer_profile/travel_relocation_form.html',
    ]  # Corresponding templates for each step

    def get(self, request, step=0, profile_id=None):
        """
        Handle the GET request to display the current step's form.
        """
        queryset = Profile.objects.filter(user=request.user)
        print(queryset)
        profile, created = Profile.objects.get_or_create(user=request.user)
        print(f'profile: {profile}')
        print(f'created: {created}')

        if created:
            print("Profile created for the user.")

        form_class = self.form_list[step]
        # profile = None
        profile_id = profile.id

        # If editing, fetch the existing profile
        if profile_id:
            profile = get_object_or_404(Profile, pk=profile_id, user=request.user)
            form = form_class(instance=profile)
        else:
            form = form_class()

        return self.render_step(request, form, step, profile_id)

    def post(self, request, step=0, profile_id=None):
        """
        Handle the POST request, saving the data and progressing to the next step.
        """
        form_class = self.form_list[step]
        profile = None

        # If editing, fetch the existing profile
        if profile_id:
            profile = get_object_or_404(Profile, pk=profile_id, user=request.user)

        form = form_class(request.POST, instance=profile)

        if form.is_valid():
            # Save the form data
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()

            # If on the last step, redirect to profile detail view or dashboard
            if step == len(self.form_list) - 1:
                print('*********************** end ')
                return redirect('freelancer_profile:profile_detail', profile_id=profile.id)

            # Otherwise, proceed to the next step
            return redirect('freelancer_profile:multi-step-edit', step=step + 1, profile_id=profile.id)

        # If the form is invalid, re-render the current step
        return self.render_step(request, form, step, profile_id)

    def render_step(self, request, form, step, profile_id):
        """
        Helper function to render the current step's form.
        """
        context = {
            'form': form,
            'step': step,
            'profile_id': profile_id,  # Pass the profile ID if editing
            'total_steps': len(self.form_list),
            'step_title': self.step_titles[step],
            'next_step': step + 1 if step + 1 < len(self.form_list) else None,  # Pass the next step value
        }

        # Use the appropriate template based on the current step
        template = self.template_list[step]
        return render(request, template, context)


@method_decorator(login_required, name='dispatch')
class ProfileDetailView(View):
    """
    View to display the profile details after the user completes the multi-step form.
    """
    def get(self, request, profile_id):
        profile = get_object_or_404(Profile, pk=profile_id, user=request.user)
        context = {'profile': profile}
        return render(request, 'freelancer_profile/profile_detail.html', context)

