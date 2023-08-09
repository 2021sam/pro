from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_datetime
from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse
from .forms import SkillForm
from .models import Skill
from django.urls import path
from .models import Experience
from django.forms import modelformset_factory
from django.forms import formset_factory




def edit(request):
    SkillModelFormSet = modelformset_factory(Skill, fields=['user', 'experience', 'skill', 'skill_years', 'skill_months'])
    if request.method == 'GET':
        skillformset = SkillModelFormSet(queryset = Skill.objects.filter(user=request.user))
        context = {'formset': skillformset}
        return render(request, 'skill/edit_set_row.html', context)

    elif request.method == 'POST':
        form = SkillModelFormSet(request.POST)
        form.save()

        skillformset = SkillModelFormSet(queryset = Skill.objects.filter(user=request.user))
        context = {'formset': skillformset}
        return render(request, 'skill/edit_set_row.html', context)



@login_required
def home(request):
    content = {}
    return render(request, 'skill/home.html', content)


@login_required
def view_summarize(request):
    skill = Skill.objects.filter(user=request.user)
    context = {'skill':  skill }
    # return render(request,'skills/view.html', context)
    d = stats(skill)
    return JsonResponse(d, safe=False)


def stats(queryset):
    count = queryset.count()
    print(count)
    d = {}
    d['count'] = count 
    for r in queryset:
        print(f'{r.skill}: {r.skill_years} years, {r.skill_months} months')
        d = add_skills(d, r.skill, r.skill_years, r.skill_months)
    return d


@login_required
def view(request):
    # skills = Skill.objects.filter(user=request.user)
    # context = {'skills':  skills }
    # return render(request,'skill/view.html', context)
    # skills = Skill.objects.filter(user=request.user)
    SkillModelFormSet = modelformset_factory(Skill, fields=['skill', 'skill_years', 'skill_months'])
    skillformset = SkillModelFormSet(queryset = Skill.objects.filter(user=request.user))
    context = {'formset': skillformset}
    return render(request, 'skill/viewset.html', context)


def add_skills(d, skill, years, months):
    if skill:
        skill = skill.lower()
        if skill not in d:
            d[skill] = 0
        d[skill] += years * 12 + months
    return d



@login_required
def add(request):
    if request.method == 'GET':
        # experience = Experience.objects.filter(author=request.user)
        # context = {'form': SkillsForm(user=request.user),
        #            'experience': experience}
        # experience = Experience.objects.filter(author=request.user)
        context = {'form': SkillForm(user=request.user)}
        return render(request,'skill/add_edit.html', context)

    elif request.method == 'POST':
        form = SkillForm(request.POST, user=request.user)
        if form.is_valid():
            experience_id = request.POST.get('experience')
            skill = request.POST.get('skill')
            skill_years = request.POST.get('skill_years')
            skill_months = request.POST.get('skill_months')
            e = Experience.objects.get(id=experience_id)
            i = Skill.objects.create(user=request.user, experience=e, skill=skill, skill_years=skill_years, skill_months=skill_months)
            print(i)
            i.save()    # For some reason it saves with out this line
            messages.success(request, 'The post has been successfully created.')
            return redirect('skill:skill-view')
        
        else:
            messages.error(request, 'Please correct the following errors:')
            return render(request,'skill/add_edit.html', {'form':form})


@login_required
def edit0(request, id):
    queryset = Skill.objects.filter(user=request.user)
    skills = get_object_or_404(queryset, pk=id)

    if request.method == 'GET':
        context = {'form': SkillForm(instance=skills, user=request.user), 'id': id}
        return render(request,'skill/add_edit.html', context)
    
    elif request.method == 'POST':
        form = SkillForm(request.POST, user=request.user, instance=skills)
        if form.is_valid():
            experience_id = request.POST.get('experience')
            skill = request.POST.get('skill')
            skill_years = request.POST.get('skill_years')
            skill_months = request.POST.get('skill_months')
            e = Experience.objects.get(id=experience_id)
            i = Skill.objects.get(id=id)
            i.experience = e
            i.skill = skill
            i.skill_years = skill_years
            i.skill_months = skill_months
            print(i)
            i.save()
            messages.success(request, 'The post has been updated successfully.')
            return redirect('skill:skill-view')

            SkillModelFormSet = modelformset_factory(Skill, fields=['skill', 'skill_years', 'skill_months'])
            skillformset = SkillModelFormSet(queryset = Skill.objects.filter(user=request.user))
            context = {'formset': skillformset}
            return render(request, 'skill/viewset.html', context)



        else:
            messages.error(request, 'Please correct the following errors:')
            return render(request,'skill/add_edit.html', {'form':form})


@login_required
def delete(request, id):
    queryset = Skill.objects.filter(user=request.user)
    skills = get_object_or_404(queryset, pk=id)
    context = {'skills': skills}

    if request.method == 'GET':
        return render(request, 'skill/delete.html', context)
    elif request.method == 'POST':
        skills.delete()
        messages.success(request,  'The post has been deleted successfully.')
        return redirect('skill:skill-view')
