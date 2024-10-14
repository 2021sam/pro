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



# /Users/2021sam/apps/zyxe/pro/freelancer_experience/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.forms import modelformset_factory
from .forms import FreelancerExperienceForm, FreelancerSkillForm
from .models import FreelancerExperience, FreelancerSkill
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@method_decorator(login_required, name='dispatch')
class MultiStepFormView(View):
    form_list = [FreelancerExperienceForm, modelformset_factory(FreelancerSkill, form=FreelancerSkillForm, extra=1, can_delete=True)]  # List of forms/formsets
    step_titles = ["Experience", "Skills"]
    template_list = [
        'freelancer_experience/experience_form.html',
        'freelancer_experience/skills_form.html'
    ]  # Templates for each step



    def get(self, request, step=0, experience_id=None):
        """
        Handle the GET request, displaying the current step's form.
        """
        form_class = self.form_list[step]

        if step == 0:  # Experience form
            form = form_class(instance=FreelancerExperience.objects.get(pk=experience_id)) if experience_id else form_class()

        elif step == 1:  # Skills formset
            formset_class = form_class
            # For new experience (experience_id is None), pass an empty queryset
            if experience_id is None:
                form = formset_class(queryset=FreelancerSkill.objects.none())
            else:
                form = formset_class(queryset=FreelancerSkill.objects.filter(experience_id=experience_id))

        return self.render_step(request, form, step, experience_id)

    def post(self, request, step=0, experience_id=None):
        """
        Handle form submission and move to the next step.
        """
        form_class = self.form_list[step]

        if step == 0:  # Experience form
            form = form_class(request.POST)

        elif step == 1:  # Skills formset
            formset_class = form_class
            form = formset_class(request.POST, queryset=FreelancerSkill.objects.filter(experience_id=experience_id) if experience_id else FreelancerSkill.objects.none())

        if form.is_valid():
            if step == 0:  # Save the experience form
                experience = form.save(commit=False)
                experience.user = request.user
                experience.save()
                request.session['experience_id'] = experience.id
                experience_id = experience.id  # Update the experience_id for the next steps

            elif step == 1:  # Save the skills formset
                skills = form.save(commit=False)
                for skill in skills:
                    skill.experience_id = experience_id
                    skill.save()

            # Move to the next step or finish
            if step + 1 < len(self.form_list):
                return redirect('freelancer_experience:multi-step-edit', step=step + 1, experience_id=experience_id)
            else:
                return redirect('freelancer_experience:experience-list')  # Redirect to the list view

        # If form is not valid, re-render the same step with the form errors
        return self.render_step(request, form, step, experience_id)

    def render_step(self, request, form, step, experience_id):
        """
        Helper function to render the current step's form.
        """
        print(f'form: {form}')
        context = {
            'formset': form if isinstance(form, type(self.form_list[1])) else None,  # Pass formset only for step 1
            'form': form if isinstance(form, FreelancerExperienceForm) else None,  # Pass the form for step 0
            'step': step,
            'total_steps': len(self.form_list),
            'step_title': self.step_titles[step],
            'experience_id': experience_id  # Pass experience_id to the template
        }

        # Use a different template based on the current step
        template = self.template_list[step]
        return render(request, template, context)
