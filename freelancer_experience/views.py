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



# from django.urls import reverse_lazy
# from django.views.generic.edit import DeleteView
# from .models import FreelancerExperience
# from django.contrib.auth.mixins import LoginRequiredMixin

# class ExperienceDeleteView(LoginRequiredMixin, DeleteView):
#     model = FreelancerExperience
#     template_name = 'freelancer_experience/experience_confirm_delete.html'  # Ensure this template exists
#     success_url = reverse_lazy('freelancer_experience:experience-list')  # Redirect after successful delete

#     def get_queryset(self):
#         # Ensure users can only delete their own experiences
#         return FreelancerExperience.objects.filter(user=self.request.user)





from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.forms import formset_factory
from .forms import FreelancerExperienceForm, FreelancerSkillForm
from .models import FreelancerExperience, FreelancerSkill
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.forms import modelformset_factory
from .forms import FreelancerExperienceForm, FreelancerSkillForm
from .models import FreelancerExperience, FreelancerSkill
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@method_decorator(login_required, name='dispatch')
class MultiStepFormView(View):
    # List of forms
    form_list = [FreelancerExperienceForm, modelformset_factory(FreelancerSkill, form=FreelancerSkillForm, extra=1, can_delete=True)]
    step_titles = ["Experience", "Skills"]
    # Corresponding templates for each form step
    template_list = [
        'freelancer_experience/experience_form.html',
        'freelancer_experience/skills_form.html',
    ]

    def get(self, request, step=0, experience_id=None):
        """
        Handle the GET request, displaying the current step's form.
        """
        form_class = self.form_list[step]

        if step == 0:
            # For step 0 (experience form), retrieve an existing experience or create a new one
            form = FreelancerExperienceForm(instance=get_object_or_404(FreelancerExperience, id=experience_id)) if experience_id else FreelancerExperienceForm()
        elif step == 1:
            # For step 1 (skills formset), use modelformset_factory to get the queryset of skills related to the experience
            form = form_class(queryset=FreelancerSkill.objects.filter(experience_id=experience_id)) if experience_id else form_class(queryset=FreelancerSkill.objects.none())
        
        return self.render_step(request, form, step, experience_id=experience_id)

    def post(self, request, step=0, experience_id=None):
        """
        Handle form submission and move to the next step.
        """
        form_class = self.form_list[step]

        if step == 0:
            # For step 0 (experience form), retrieve the instance or create a new one
            form = FreelancerExperienceForm(request.POST, instance=get_object_or_404(FreelancerExperience, id=experience_id)) if experience_id else FreelancerExperienceForm(request.POST)
        elif step == 1:
            # For step 1 (skills formset), bind the POST data
            form = form_class(request.POST)

        if form.is_valid():
            if step == 0:
                # Save the experience form and store experience_id in the session
                experience = form.save(commit=False)
                experience.user = request.user
                experience.save()
                request.session['experience_id'] = experience.id
                return redirect(reverse('freelancer_experience:multi-step-edit', kwargs={'step': 1, 'experience_id': experience.id}))
            elif step == 1:
                # Save the skill formset
                skills = form.save(commit=False)
                for skill in skills:
                    skill.experience_id = request.session['experience_id']
                    skill.save()
                return redirect('freelancer_experience:experience-list')

        return self.render_step(request, form, step, experience_id=experience_id)

    def render_step(self, request, form, step, experience_id=None):
        """
        Helper function to render the current step's form.
        """
        context = {
            'form': form,
            'step': step,
            'experience_id': experience_id,
            'total_steps': len(self.form_list),
            'step_title': self.step_titles[step],
            'next_step': step + 1 if step + 1 < len(self.form_list) else None,
        }

        # Use the appropriate template based on the current step
        template = self.template_list[step]
        return render(request, template, context)
