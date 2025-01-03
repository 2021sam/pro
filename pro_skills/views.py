# # /Users/2021sam/apps/zyxe/pro/pro_skills/views.py
# # views.py
# from django.shortcuts import render, redirect, get_object_or_404
# from .models import Skill
# from .forms import SkillForm, SkillFormSet
# from django.forms import modelformset_factory

# def skill_create_view(request):
#     # Use modelformset_factory to create a formset for Skill model
#     SkillFormSet = modelformset_factory(Skill, form=SkillForm, extra=1)
#     if request.method == 'POST':
#         formset = SkillFormSet(request.POST)
#         if formset.is_valid():
#             instances = formset.save(commit=False)
#             for instance in instances:
#                 instance.user = request.user
#                 instance.save()
#             formset.save_m2m()  # Save many-to-many relationships if needed
#             return redirect('skill_list')
#         else:
#             print('Formset Errors:', formset.errors)
#     else:
#         formset = SkillFormSet(queryset=Skill.objects.none())  # Show empty formset for new entries

#     # Render the formset in the template for creating multiple skills
#     return render(request, 'skill/skill_formset.html', {'formset': formset, 'form_type': 'create'})

# def skill_edit_view(request, pk):
#     skill = get_object_or_404(Skill, pk=pk)
#     if request.method == 'POST':
#         form = SkillForm(request.POST, instance=skill)
#         if form.is_valid():
#             form.save()
#             return redirect('skill_list')
#     else:
#         form = SkillForm(instance=skill)

#     # Render the single form in the template for editing an existing skill
#     return render(request, 'skill/skill_form.html', {'form': form, 'form_type': 'edit'})

# def skill_list_view(request):
#     skills = Skill.objects.all()
#     return render(request, 'skill/skill_list.html', {'skills': skills})



# def skill_delete_view(request, pk):
#     skill = get_object_or_404(Skill, pk=pk)
#     if request.method == 'POST':
#         skill.delete()
#         return redirect('skill_list')
#     return render(request, 'skill/skill_confirm_delete.html', {'skill': skill})
