# /Users/2021sam/apps/zyxe/pro/pro_experience/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Experience
from .forms import ExperienceForm
from pro_skills.forms import SkillFormSet
from pro_skills.models import Skill

@login_required
def home(request):
    content = {}
    return render(request, 'pro_experience/home.html', content)

@login_required
def view(request):
    experience_list = Experience.objects.filter(user=request.user)
    context = {'experience_list': experience_list}
    return render(request, 'pro_experience/experience_list.html', context)

@login_required
def add_edit_experience(request, experience_id=None):
    # Fetch experience if experience_id is provided (edit case), otherwise create new (add case)
    if experience_id:
        experience = get_object_or_404(Experience, pk=experience_id)
        experience_form = ExperienceForm(instance=experience)
        formset = SkillFormSet(queryset=Skill.objects.filter(experience=experience))
    else:
        experience = None
        experience_form = ExperienceForm()
        formset = SkillFormSet(queryset=Skill.objects.none())

    if request.method == 'POST':
        experience_form = ExperienceForm(request.POST, instance=experience)
        formset = SkillFormSet(request.POST, queryset=Skill.objects.filter(experience=experience) if experience else Skill.objects.none())

        if experience_form.is_valid() and formset.is_valid():
            # Save the experience
            experience = experience_form.save(commit=False)
            experience.user = request.user  # Set the current logged-in user
            experience.save()

            # Save the skills associated with the experience
            skills = formset.save(commit=False)
            for skill in skills:
                skill.experience = experience
                skill.user = request.user
                skill.save()

            # Handle deletions if any
            for obj in formset.deleted_objects:
                obj.delete()

            formset.save()  # Ensure formset is saved

            return redirect('pro_experience:experience-view')

    return render(request, 'pro_experience/experience_form.html', {
        'experience_form': experience_form,
        'formset': formset,
        'experience': experience,
    })

@login_required
def delete(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
    if request.method == 'POST':
        experience.delete()
        return redirect('pro_experience:experience-view')
    return render(request, 'pro_experience/experience_confirm_delete.html', {'experience': experience})




# # /Users/2021sam/apps/zyxe/pro/pro_experience/views.py

# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.utils.dateparse import parse_datetime
# from django.contrib import messages
# from django.http import HttpResponse
# from .models import Experience
# from .forms import ExperienceForm
# from pro_skills.forms import SkillFormSet
# from pro_skills.models import Skill


# @login_required
# def home(request):
#     content = {}
#     return render(request, 'pro_experience/home.html', content)


# @login_required
# def view(request):
#     experiences = Experience.objects.filter(user=request.user)
#     context = {'experiences': experiences}
#     return render(request, 'pro_experience/experience_list.html', context)


# @login_required
# def add_edit_experience_with_skills(request, experience_id=None):
#     # Fetch the experience if experience_id is provided (edit case), otherwise create new (add case)
#     if experience_id:
#         experience = get_object_or_404(Experience, pk=experience_id)
#         experience_form = ExperienceForm(instance=experience)
#         formset = SkillFormSet(queryset=Skill.objects.filter(experience=experience))
#     else:
#         experience = None
#         experience_form = ExperienceForm()
#         formset = SkillFormSet(queryset=Skill.objects.none())

#     if request.method == 'POST':
#         experience_form = ExperienceForm(request.POST, instance=experience)
#         formset = SkillFormSet(request.POST, queryset=Skill.objects.filter(experience=experience) if experience else Skill.objects.none())

#         # Validate both the experience form and formset
#         if experience_form.is_valid() and formset.is_valid():
#             print('pro_experience/views.py: formset.is_valid')

#             # Save the experience
#             experience = experience_form.save(commit=False)
#             experience.user = request.user  # Set the current logged-in user
#             experience.save()

#             # Save the skills and handle deletions automatically
#             skills = formset.save(commit=False)
#             for skill in skills:
#                 skill.experience = experience  # Assign the saved experience to each skill
#                 skill.user = request.user  # Set the current logged-in user for each skill
#                 skill.save()

#             # Handle deletions manually if using commit=False
#             for obj in formset.deleted_objects:
#                 print(f'Deleting skill: {obj.skill}, Years: {obj.skill_years}, Months: {obj.skill_months}')
#                 obj.delete()

#             # Save the formset to ensure deletions are handled
#             formset.save()

#             return redirect('pro_experience:experience-view')  # Adjust to your desired redirect URL
#         else:
#             print("Experience form errors:", experience_form.errors)
#             print("Formset errors:", formset.errors)

#     return render(request, 'pro_experience/experience_form.html', {
#         'experience_form': experience_form,
#         'formset': formset,
#         'experience': experience,
#         'experience_id': experience_id
#     })


# @login_required
# def delete(request, experience_id):
#     queryset = Experience.objects.filter(user=request.user)
#     experience = get_object_or_404(queryset, pk=experience_id)
#     context = {'experience': experience}
    
#     if request.method == 'GET':
#         return render(request, 'pro_experience/experience_delete_confirmation.html', context)
#     elif request.method == 'POST':
#         experience.delete()
#         messages.success(request, 'The experience has been deleted successfully.')
#         return redirect('pro_experience:experience-view')












# # from django.shortcuts import render, redirect, get_object_or_404
# # from django.contrib.auth.decorators import login_required
# # from django.utils.dateparse import parse_datetime
# # from django.contrib import messages
# # from django.http import HttpResponse
# # from .models import Experience
# # from .forms import ExperienceForm
# # from django.urls import path



# # @login_required
# # def home(request):
# #     content = {}
# #     return render(request, 'experience/home.html', content)


# # @login_required
# # def view(request):
# #     experience = Experience.objects.filter(user=request.user)
# #     context = {'experience':  experience }
# #     return render(request,'experience/view.html', context)


# # @login_required
# # def add(request):
# #     if request.method == 'GET':
# #         context = {'form': ExperienceForm()}
# #         return render(request,'experience/add_edit.html', context)
    
# #     elif request.method == 'POST':
# #         form = ExperienceForm(request.POST)
# #         if form.is_valid():
# #             i = form.save(commit=False)
# #             i.user = request.user
# #             i.duration = i.date_end - i.date_start
# #             i.duration_days = i.duration.days  # Correctly extracts the number of days from the duration
# #             i.save()
# #             messages.success(request, 'The post has been successfully created.')
# #             return redirect('experience-view')
# #         else:
# #             messages.error(request, 'Please correct the following errors:')
# #             return render(request,'experience/add_edit.html', {'form':form})  


# # @login_required    
# # def edit(request, id):
# #     queryset = Experience.objects.filter(user=request.user)
# #     experience = get_object_or_404(queryset, pk=id)

# #     if request.method == 'GET':
# #         context = {'form': ExperienceForm(instance=experience), 'id': id}
# #         return render(request,'experience/add_edit.html', context)
    
# #     elif request.method == 'POST':
# #         form = ExperienceForm(request.POST, instance=experience)
# #         if form.is_valid():
# #             i = form.save(commit=False)
# #             i.duration = i.date_end - i.date_start
# #             i.duration_days = i.duration.days  # Correctly extracts the number of days from the duration
# #             form.save()
# #             messages.success(request, 'The post has been updated successfully.')
# #             return redirect('experience-view')
# #         else:
# #             messages.error(request, 'Please correct the following errors:')
# #             return render(request,'experience/add_edit.html', {'form':form})


# # @login_required
# # def delete(request, id):
# #     queryset = Experience.objects.filter(user=request.user)
# #     experience = get_object_or_404(queryset, pk=id)
# #     context = {'experience': experience}
    
# #     if request.method == 'GET':
# #         return render(request, 'experience/delete.html', context)
# #     elif request.method == 'POST':
# #         experience.delete()
# #         messages.success(request,  'The post has been deleted successfully.')
# #         return redirect('experience-view')
