# /Users/2021sam/apps/zyxe/pro/freelancer_experience/views.py
from django.shortcuts import render, redirect
from django.views import View
from django.forms import formset_factory
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


@method_decorator(login_required, name='dispatch')  # Ensure all methods require login
class MultiStepFormView(View):
    form_list = [FreelancerExperienceForm, formset_factory(FreelancerSkillForm, extra=1)]  # List of forms
    step_titles = ["Experience", "Skills", "Manager Info", "Location Info"]
    template_list = [
        'freelancer_experience/experience_form.html',
        'freelancer_experience/skills_form.html',
        'freelancer_experience/manager_form.html',
        'freelancer_experience/location_form.html'
    ]  # Corresponding templates for each form step

    def get(self, request, step=0):
        """
        Handle the GET request, displaying the current step's form.
        """
        form_class = self.form_list[step]
        if step == 0:
            form = form_class() if not isinstance(form_class, list) else form_class(queryset=FreelancerSkill.objects.none())
        
        if step == 1:
            form = form_class(queryset=FreelancerSkill.objects.none())
    
        return self.render_step(request, form, step)

    def post(self, request, step=0):
        """
        Handle form submission and move to the next step.
        """
        form_class = self.form_list[step]
        form = form_class(request.POST) if not isinstance(form_class, list) else form_class(request.POST)

        if form.is_valid():
            # Save the form data in session or DB (based on the step)
            if step == 0:
                experience = form.save(commit=False)
                experience.user = request.user
                experience.save()
                request.session['experience_id'] = experience.id  # Save ID in session for later use
            elif step == 1:
                skills = form.save(commit=False)
                for skill in skills:
                    skill.experience_id = request.session['experience_id']
                    skill.save()
            else:
                # Handle manager and location form data (Steps 2 and 3)
                experience_id = request.session.get('experience_id')
                if experience_id:
                    experience = FreelancerExperience.objects.get(id=experience_id)
                    if step == 2:
                        experience.manager_name = form.cleaned_data['manager_name']
                        experience.manager_email = form.cleaned_data['manager_email']
                        experience.manager_phone = form.cleaned_data['manager_phone']
                    elif step == 3:
                        experience.on_site_work_city = form.cleaned_data['on_site_work_city']
                        experience.on_site_work_state = form.cleaned_data['on_site_work_state']
                        experience.location_remote = form.cleaned_data['location_remote']
                        experience.location_hybrid = form.cleaned_data['location_hybrid']
                    experience.save()

            # Move to the next step, or finish
            if step + 1 < len(self.form_list):
                return redirect('freelancer_experience:multi-step', step=step + 1)
            else:
                return redirect('freelancer_experience:experience-list')  # Redirect to final view after all steps are done

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
            'next_step': step + 1 if step + 1 < len(self.form_list) else None,  # Pass the next step value
        }

        # Use a different template based on the current step
        template = self.template_list[step]
        return render(request, template, context)
