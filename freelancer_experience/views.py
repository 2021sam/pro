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


from django.forms import modelformset_factory
from .forms import FreelancerExperienceForm, FreelancerSkillForm
from .models import FreelancerExperience, FreelancerSkill

from django.forms import modelformset_factory
from .forms import FreelancerExperienceForm, FreelancerSkillForm
from .models import FreelancerExperience, FreelancerSkill

from django.shortcuts import render, redirect
from django.views import View
from django.forms import formset_factory
from .forms import FreelancerExperienceForm, FreelancerSkillFormSet
from .models import FreelancerExperience, FreelancerSkill
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')  # Ensure all methods require login
class MultiStepFormView(View):
    form_list = [FreelancerExperienceForm, FreelancerSkillFormSet]  # List of forms
    step_titles = ["Experience", "Skills"]
    template_list = [
        'freelancer_experience/experience_form.html',
        'freelancer_experience/skills_form.html'
    ]

    def get(self, request, step=0):
        """
        Handle the GET request, displaying the current step's form.
        """
        if step == 0:
            form = self.form_list[step]()
        elif step == 1:
            form = self.form_list[step](queryset=FreelancerSkill.objects.none())  # Pass formset for skills

        return self.render_step(request, form, step)

    def post(self, request, step=0):
        """
        Handle form submission and move to the next step.
        """
        if step == 0:
            form = self.form_list[step](request.POST)
        elif step == 1:
            form = self.form_list[step](request.POST)

        if form.is_valid():
            # Save form data based on the step
            if step == 0:
                experience = form.save(commit=False)
                experience.user = request.user
                experience.save()
                request.session['experience_id'] = experience.id
            elif step == 1:
                experience_id = request.session.get('experience_id')
                print(f'79 experience_id: {experience_id}')
                experience = FreelancerExperience.objects.get(id=experience_id)
                print(f'experience: {experience}')
                skills = form.save(commit=False)
                for skill in skills:
                    skill.experience = experience
                    skill.save()

            # Move to the next step or finish
            if step + 1 < len(self.form_list):
                return redirect('freelancer_experience:multi-step', step=step + 1)
            else:
                return redirect('freelancer_experience:experience-list')

        return self.render_step(request, form, step)

    def render_step(self, request, form, step):
        """
        Helper function to render the current step's form.
        """
        context = {
            'form': form,
            'step': step,
            'total_steps': len(self.form_list),
            'step_title': self.step_titles[step],
        }

        template = self.template_list[step]
        return render(request, template, context)




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
