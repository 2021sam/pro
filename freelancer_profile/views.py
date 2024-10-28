# /Users/2021sam/apps/zyxe/pro/freelancer_profile/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError

from .models import FreelancerProfile
from .forms import PersonalInfoForm, EmploymentPreferencesForm, LocationPreferencesForm, TravelRelocationForm, \
    DesiredTitleForm


@method_decorator(login_required, name='dispatch')  # Ensure all methods require login
class ProfileMultiStepFormView(View):
    form_list = [
        PersonalInfoForm,
        EmploymentPreferencesForm,
        LocationPreferencesForm,
        TravelRelocationForm,
        DesiredTitleForm
    ]  # List of forms for each step
    step_titles = ["Personal Information", "Employment Preferences", "Location Preferences", "Travel & Relocation", "Desired Job Title"]  # Titles for each step
    template_list = [
        'freelancer_profile/personal_info_form.html',
        'freelancer_profile/employment_preferences_form.html',
        'freelancer_profile/location_preferences_form.html',
        'freelancer_profile/travel_relocation_form.html',
        'freelancer_profile/desired_job_title_form.html',
    ]  # Corresponding templates for each step


    def get(self, request, step=0):
        """
        Handle the GET request to display the current step's form.
        """
        # queryset = Profile.objects.filter(user=request.user)
        # print(queryset)
        profile, created = FreelancerProfile.objects.get_or_create(user=request.user)
        print(f'profile: {profile}')
        print(f'created: {created}')

        if created:
            print("Profile created for the user.")

        form_class = self.form_list[step]
        profile_id = profile.id
        print(f'profile_id: {profile_id}')

        # If editing, fetch the existing profile
        if profile_id:
            profile = get_object_or_404(FreelancerProfile, pk=profile_id, user=request.user)
            form = form_class(instance=profile)
        else:
            form = form_class()

        return self.render_step(request, form, step, profile_id)

    def post(self, request, step=0):
        """
        Handle the POST request, saving the data and progressing to the next step.
        """
        print(f'ProfileMultiStepFormView: step: {step}')
        # print(f'ProfileMultiStepFormView: profile_id: {profile_id}')

        # Fetch or create the Profile based on the current user
        profile, created = FreelancerProfile.objects.get_or_create(user=request.user)
        print(f'profile: {profile}')

        form_class = self.form_list[step]
        form = form_class(request.POST, instance=profile)

        if form.is_valid():
            # Save the form data
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()

            # If on the last step, redirect to profile detail view or dashboard
            if step == len(self.form_list) - 1:
                print('*********************** end ')
                return redirect('home')

            # Otherwise, proceed to the next step
            return redirect('freelancer_profile:multi-step-edit', step=step + 1)

        # If the form is invalid, re-render the current step
        return self.render_step(request, form, step, profile.id)

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
        profile = get_object_or_404(FreelancerProfile, pk=profile_id, user=request.user)
        context = {'profile': profile}
        return render(request, 'freelancer_profile/profile_detail.html', context)


# # views.py
# from django.views.generic import DetailView
# from .models import FreelancerProfile
# from pro_education.models import Education
# from freelancer_experience.models import FreelancerExperience, FreelancerSkill
#
# class FreelancerDetailView(DetailView):
#     model = FreelancerProfile
#     template_name = 'freelancer_profile/freelancer_profile_detail.html'
#     context_object_name = 'freelancer'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['education'] = Education.objects.filter(freelancer=self.object)
#         context['experience'] = FreelancerExperience.objects.filter(freelancer=self.object)
#         context['skills'] = FreelancerSkill.objects.filter(freelancer=self.object)
#         return context


# /Users/2021sam/apps/zyxe/pro/freelancer_profile/views.py
from django.shortcuts import render, get_object_or_404
from .models import FreelancerProfile
from pro_education.models import Education
from freelancer_experience.models import FreelancerExperience, FreelancerSkill


class FreelancerDetailView(View):
    def get(self, request, pk):
        # Get the freelancer's profile
        freelancer = get_object_or_404(FreelancerProfile, pk=pk)

        # Get freelancer's education records
        education = Education.objects.filter(user=freelancer.user)

        # Get freelancer's experience and related skills
        experiences = FreelancerExperience.objects.filter(user=freelancer.user)
        skills = FreelancerSkill.objects.filter(experience__user=freelancer.user)

        # Context to pass to the template
        context = {
            'freelancer': freelancer,
            'education': education,
            'experiences': experiences,
            'skills': skills,
        }

        return render(request, 'freelancer_profile/freelancer_profile_detail.html', context)
