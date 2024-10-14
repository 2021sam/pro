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

@method_decorator(login_required, name='dispatch')
class ExperienceDeleteView(DeleteView):
    model = FreelancerExperience
    template_name = 'freelancer_experience/experience_confirm_delete.html'
    context_object_name = 'experience'
    success_url = reverse_lazy('freelancer_experience:experience-list')

    def get_object(self):
        """Override this method to ensure only the user's experience can be deleted."""
        experience_id = self.kwargs.get('experience_id')
        experience = get_object_or_404(FreelancerExperience, pk=experience_id, user=self.request.user)
        return experience




from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.forms import formset_factory
from .forms import FreelancerExperienceForm, FreelancerSkillForm
from .models import FreelancerExperience, FreelancerSkill
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

@method_decorator(login_required, name='dispatch')
class MultiStepFormView(View):
    form_list = [FreelancerExperienceForm, formset_factory(FreelancerSkillForm, extra=1)]  # List of forms
    step_titles = ["Experience", "Skills", "Manager Info", "Location Info"]
    template_list = [
        'freelancer_experience/experience_form.html',
        'freelancer_experience/skills_form.html',
        'freelancer_experience/manager_form.html',
        'freelancer_experience/location_form.html'
    ]  # Corresponding templates for each form step



    def get(self, request, step=0, experience_id=None):
        """
        Handle the GET request, displaying the current step's form.
        """
        form_class = self.form_list[step]
        
        if step == 0:  # Experience form
            if experience_id:
                experience = get_object_or_404(FreelancerExperience, id=experience_id, user=request.user)
                form = FreelancerExperienceForm(instance=experience)
            else:
                form = FreelancerExperienceForm()
        
        elif step == 1:  # Skill formset
            FreelancerSkillFormSet = formset_factory(FreelancerSkillForm, extra=1, can_delete=True)
            if experience_id:
                experience = get_object_or_404(FreelancerExperience, id=experience_id, user=request.user)
                form = FreelancerSkillFormSet(queryset=FreelancerSkill.objects.filter(experience=experience))
            else:
                form = FreelancerSkillFormSet(queryset=FreelancerSkill.objects.none())

        return self.render_step(request, form, step)


    def post(self, request, step=0, experience_id=None):
        """
        Handle form submission and move to the next step.
        """
        form_class = self.form_list[step]

        if step == 0:  # Experience form submission
            if experience_id:
                experience = get_object_or_404(FreelancerExperience, id=experience_id, user=request.user)
                form = FreelancerExperienceForm(request.POST, instance=experience)
            else:
                form = FreelancerExperienceForm(request.POST)

            if form.is_valid():
                experience = form.save(commit=False)
                experience.user = request.user
                experience.save()
                request.session['experience_id'] = experience.id  # Save experience ID
                experience_id = experience.id  # Update experience_id for future steps

                return redirect('freelancer_experience:multi-step-edit', step=1, experience_id=experience.id)

        elif step == 1:  # Skill formset submission
            FreelancerSkillFormSet = formset_factory(FreelancerSkillForm, extra=1, can_delete=True)
            form = FreelancerSkillFormSet(request.POST)

            if form.is_valid():
                skills = form.save(commit=False)
                for skill in skills:
                    skill.experience_id = request.session['experience_id']
                    skill.save()

                return redirect('freelancer_experience:multi-step-edit', step=2, experience_id=experience_id)

        return self.render_step(request, form, step)





    # def get(self, request, step=0, experience_id=None):
    #     """
    #     Handle the GET request, displaying the current step's form. Load the instance if editing.
    #     """
    #     form_class = self.form_list[step]

    #     # If this is an edit, load the experience instance
    #     if experience_id and step == 0:
    #         experience = get_object_or_404(FreelancerExperience, id=experience_id, user=request.user)
    #         form = form_class(instance=experience)  # Prepopulate form with experience data
    #     elif step == 1 and experience_id:
    #         experience = get_object_or_404(FreelancerExperience, id=experience_id, user=request.user)
    #         formset = form_class(queryset=FreelancerSkill.objects.filter(experience=experience))
    #         return self.render_step(request, formset, step)
    #     else:
    #         # If adding a new experience
    #         form = form_class()

    #     return self.render_step(request, form, step)

    # def post(self, request, step=0, experience_id=None):
    #     """
    #     Handle form submission and move to the next step. Load the instance if editing.
    #     """
    #     form_class = self.form_list[step]
    #     form = form_class(request.POST) if not isinstance(form_class, list) else form_class(request.POST)

    #     if form.is_valid():
    #         if step == 0:
    #             if experience_id:
    #                 experience = get_object_or_404(FreelancerExperience, id=experience_id, user=request.user)
    #                 form = FreelancerExperienceForm(request.POST, instance=experience)
    #             else:
    #                 experience = form.save(commit=False)
    #                 experience.user = request.user
    #                 experience.save()
    #                 request.session['experience_id'] = experience.id  # Save ID in session for later use
    #                 experience_id = experience.id  # Update experience_id for future steps

    #         elif step == 1:
    #             skills = form.save(commit=False)
    #             for skill in skills:
    #                 skill.experience_id = request.session['experience_id']
    #                 skill.save()

    #         # Move to the next step or finish
    #         if step + 1 < len(self.form_list):
    #             return redirect('freelancer_experience:multi-step-edit', step=step + 1, experience_id=experience_id)
    #         else:
    #             return redirect('freelancer_experience:experience-list')

    #     return self.render_step(request, form, step)


    def render_step(self, request, form, step):
        """
        Helper function to render the current step's form.
        """
        context = {
            'form': form,
            'step': step,
            'total_steps': len(self.form_list),
            'step_title': self.step_titles[step],
            'next_step': step + 1 if step + 1 < len(self.form_list) else None,
        }

        template = self.template_list[step]
        return render(request, template, context)
