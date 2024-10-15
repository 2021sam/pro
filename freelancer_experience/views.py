# /Users/2021sam/apps/zyxe/pro/freelancer_experience/views.py
from django.shortcuts import render, redirect
from django.views import View
from django.forms import modelformset_factory
from .forms import FreelancerExperienceForm, FreelancerSkillForm
from .models import FreelancerExperience, FreelancerSkill
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class Home(View):
    def get(self, request):
        content = {}
        return render(request, 'freelancer_experience/home.html', content)


@method_decorator(login_required, name='dispatch')  # Ensure all methods require login
class ExperienceList(View):
    def get(self, request):
        experience_list = FreelancerExperience.objects.filter(user=request.user)
        context = {'experience_list': experience_list}
        return render(request, 'freelancer_experience/experience_list.html', context)


from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import DeleteView
from .models import FreelancerExperience

# @method_decorator(login_required, name='dispatch')
# class ExperienceDeleteView(DeleteView):
#     model = FreelancerExperience
#     template_name = 'freelancer_experience/experience_confirm_delete.html'
#     context_object_name = 'experience'
#     success_url = reverse_lazy('freelancer_experience:experience-list')

#     def get_object(self):
#         """Override this method to ensure only the user's experience can be deleted."""
#         experience_id = self.kwargs.get('experience_id')
#         experience = get_object_or_404(FreelancerExperience, pk=experience_id, user=self.request.user)
#         return experience

# /Users/2021sam/apps/zyxe/pro/freelancer_experience/views.py

from django.urls import reverse_lazy
from django.views.generic import DeleteView
from .models import FreelancerExperience

class ExperienceDeleteView(DeleteView):
    model = FreelancerExperience
    template_name = 'freelancer_experience/experience_confirm_delete.html'
    success_url = reverse_lazy('freelancer_experience:experience-list')  # Redirect after deletion



from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.forms import modelformset_factory
from .forms import FreelancerExperienceForm, FreelancerSkillForm
from .models import FreelancerExperience, FreelancerSkill
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@method_decorator(login_required, name='dispatch')  # Ensure all methods require login
class MultiStepFormView(View):
    form_list = [FreelancerExperienceForm, modelformset_factory(FreelancerSkill, form=FreelancerSkillForm, extra=1, can_delete=True)]  # List of forms/formsets
    step_titles = ["Experience", "Skills"]  # Titles for each step
    template_list = [
        'freelancer_experience/experience_form.html',
        'freelancer_experience/skills_form.html',
    ]  # Corresponding templates for each step

    def get(self, request, step=0, experience_id=None):
        """
        Handle the GET request to display the current step's form or formset.
        """
        form_class = self.form_list[step]
        experience = None
        formset = None

        # If editing, fetch the existing experience
        if experience_id:
            experience = get_object_or_404(FreelancerExperience, pk=experience_id)
            form = form_class(instance=experience) if step == 0 else form_class(queryset=FreelancerSkill.objects.filter(experience=experience))
        else:
            form = form_class() if step == 0 else form_class(queryset=FreelancerSkill.objects.none())

        # Handle formset separately for the skills step (step 1)
        if step == 1:
            formset = form
            form = None

        return self.render_step(request, form, formset, step, experience_id)


    def post_skills(self, request, formset):
        # Validate the formset
        # Save the skills formset
        skills = formset.save(commit=False)
        for skill in skills:
            skill.experience_id = request.session['experience_id']
            skill.save()

        # Handle deletions if any
        for obj in formset.deleted_objects:
            obj.delete()
        formset.save()  # Ensure formset is saved


    def post(self, request, step=0, experience_id=None):
        """
        Handle the POST request, saving the data and progressing to the next step.
        """

        form_class = self.form_list[step]
        experience = None

        # If editing, fetch the existing experience
        if experience_id:
            experience = get_object_or_404(FreelancerExperience, pk=experience_id)

        print(f'step: {step}')
        if step == 0:
            form = form_class(request.POST, instance=experience)
            if form.is_valid():
                # Save the experience form
                experience = form.save(commit=False)
                experience.user = request.user
                experience.save()
                request.session['experience_id'] = experience.id  # Save the experience ID in the session
                return redirect('freelancer_experience:multi-step-edit', step=step + 1, experience_id=experience.id)
            return self.render_step(request, form, None, step, experience_id)

        if step == 1:
            # Initialize the form or formset based on the step
            formset = form_class(request.POST)
            if formset.is_valid():
                self.post_skills(request, formset)
                return redirect('freelancer_experience:experience-list')  # Redirect to the experience list after completion)
            return self.render_step(request, None, formset, step, experience_id)


    def render_step(self, request, form, formset, step, experience_id):
        """
        Helper function to render the current step's form or formset.
        """
        context = {
            'form': form,
            'formset': formset,  # Pass the formset separately if applicable
            'step': step,
            'experience_id': experience_id,  # Pass the experience ID if editing
            'total_steps': len(self.form_list),
            'step_title': self.step_titles[step],
            'next_step': step + 1 if step + 1 < len(self.form_list) else None,  # Pass the next step value
        }

        # Use the appropriate template based on the current step
        template = self.template_list[step]
        return render(request, template, context)
