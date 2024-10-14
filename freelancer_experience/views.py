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

@method_decorator(login_required, name='dispatch')
class MultiStepFormView(View):
    form_list = [FreelancerExperienceForm, FreelancerSkillFormSet]
    step_titles = ["Experience", "Skills"]
    template_list = [
        'freelancer_experience/experience_form.html',
        'freelancer_experience/skills_form.html'
    ]

    def get(self, request, step=0):
        """
        Handle the GET request, displaying the current step's form.
        """
        form_class = self.form_list[step]
        if step == 0:
            form = form_class()
        elif step == 1:
            form = form_class(queryset=FreelancerSkill.objects.none())
        
        return self.render_step(request, form, step)

    def post(self, request, step=0):
        """
        Handle form submission and move to the next step.
        """
        form_class = self.form_list[step]
        if step == 0:
            form = form_class(request.POST)
        elif step == 1:
            form = form_class(request.POST)

        if form.is_valid():
            # Save the form data
            if step == 0:
                # Save the experience
                experience = form.save(commit=False)
                experience.user = request.user
                experience.save()
                request.session['experience_id'] = experience.id  # Save experience ID in session
            elif step == 1:
                # Save the skills and link them to the experience
                skills = form.save(commit=False)
                experience_id = request.session.get('experience_id')
                experience = FreelancerExperience.objects.get(id=experience_id)
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
