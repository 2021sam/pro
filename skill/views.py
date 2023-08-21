from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.dateparse import parse_datetime
from django.http import HttpResponse, JsonResponse, QueryDict
from django.forms import modelformset_factory
from .forms import SkillForm
from .models import Skill
from .models import Experience
from django.views.decorators.http import require_http_methods
# Reference:
# https://docs.djangoproject.com/en/4.2/topics/forms/modelforms/#model-formsets



def edit_hx(request):
    print('edit_hx')

    if request.method == 'GET':
        SkillModelFormSet = modelformset_factory(Skill, form=SkillForm, extra=0, can_delete=True)
        queryset = Skill.objects.filter(user=request.user)
        # print(queryset.count)
        # print(len(queryset))
        # print(queryset[0].experience)
        # https://stackoverflow.com/questions/622982/django-passing-custom-form-parameters-to-formset
        skillformset = SkillModelFormSet(form_kwargs={'user': request.user}, queryset = Skill.objects.filter(user=request.user))
        skillform = SkillForm(user=request.user)
        context = {'formset': skillformset, 'skillform': skillform}
        return render(request, 'skill/hx_skills.html', context)

    elif request.method == 'POST':
        print("POST")
        print(f'POST: {request.POST}')
        print(f'FILES: {request.FILES}')
        form = SkillForm(request.POST, request.FILES, user=request.user)
        print(form)
        print(f'form.is_bound1 = {form.is_bound}')
        print(f'form.has_changed() = {form.has_changed()}')
        print(f'form.is_valid() = {form.is_valid()}')       # Need required=True but gives form not valid

        d = {}
        for key, value in request.POST.lists():
            print(key, value)
            field = key.split('-')
            print(field)
            print( len(field))
            if len(field) == 1:
                d[field[0]] = value[0]

            if len(field) == 3:
                d[field[2]] = value[0]

        skills = list(d.keys())
        print(f'skills: {skills}')
        skills.sort()
        print(f'skills_sorted: {skills}')
        d_sorted = { i: d[i] for i in skills }
        print(d_sorted)
        # d = {}
        # for key in request.POST.lists():
        #     d[key] = request.POST.lists(key)
        print('************************************')
        print(d)
        print('************************************')
        if len(d) < 5:
            print(f'Not enough elements to save {len(d)}')
            return HttpResponse('')
        
        id = int(d['id'])
        experience_id = int(d['experience'])
        skill = d['skill']
        skill_years = int(d['skill_years'])
        skill_months = int(d['skill_months'])
        e = Experience.objects.get(id=experience_id)

        if id == 0:
            id = 0
            i = Skill(user=request.user, experience_id = experience_id, skill = skill, skill_years = skill_years, skill_months=skill_months)
            i.save()
            SkillModelFormSet = modelformset_factory(Skill, form=SkillForm, extra=0, can_delete=True)
            queryset = Skill.objects.filter(user=request.user)
            skillformset = SkillModelFormSet(form_kwargs={'user': request.user}, queryset = Skill.objects.filter(user=request.user))
            skillform = SkillForm(user=request.user)
            context = {'formset': skillformset, 'skillform': skillform}

            # context = {'formset': skillformset}
            return render(request, 'skill/hx_skills.html', context)


            # SkillModelFormSet = modelformset_factory(Skill, form=SkillForm, extra=0, can_delete=True)
            # queryset = Skill.objects.filter(user=request.user)

            # skillformset = SkillModelFormSet(form_kwargs={'user': request.user}, queryset = Skill.objects.filter(user=request.user))
            # skillform = SkillForm(user=request.user)
            # context = {'formset': skillformset, 'skillform': skillform}
            # return render(request, 'skill/hx_skills.html', context)



        if id:
            i = Skill.objects.get(id=id)
            i.experience = e
            i.skill = skill
            i.skill_years = skill_years
            i.skill_months = skill_months
            print(i)
            i.save()
            print('****************************************     saved')
            return HttpResponse('')
    

        #     if form.has_changed():
        #         messages.success(request, f'The post has been successfully saved.')
        #         return redirect('')
        #     else:
        #         messages.success(request, f'No changes made.')
        #         return redirect('')

        # else:
        #     for error in form.errors:
        #         print(error)
        
        #     messages.error(request, 'Please correct the following errors:')
        #     context = {'formset': form}
        #     return render(request, 'skill/edit_set_row.html', context)










def edit(request):
    SkillModelFormSet = modelformset_factory(Skill, form=SkillForm, extra=3)
    if request.method == 'GET':
        # https://stackoverflow.com/questions/622982/django-passing-custom-form-parameters-to-formset
        # skillformset = SkillModelFormSet(form_kwargs={'user': request.user}, queryset = (Skill.objects.filter(user=request.user)))
        skillformset = SkillModelFormSet(form_kwargs={'user': request.user}, queryset = Skill.objects.filter(user=request.user).order_by('skill') )
        queryset = Skill.objects.filter(user=request.user)

        d = {}
        for skill in queryset:
            print(skill.id, skill.skill, skill.skill_years )
            if skill.skill not in d:
                d[skill.skill] = 0
            d[skill.skill] += skill.skill_years * 12
            d[skill.skill] += skill.skill_months

#         student_tuples = [
# ...     ('john', 'A', 15),
# ...     ('jane', 'B', 12),
# ...     ('dave', 'B', 10),
# ... ]
# >>> sorted(student_tuples, key=lambda student: student[2])   # sort by age
# [('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]

        print('********************')
        print(d)
        skill_list = list(d.keys())
        print(skill_list)
        print('.')
        skill_list.sort()
        print(skill_list)

        print('.')
        d_sorted = {i: d[i] for i in skill_list}
        print('.')
        print(d_sorted)

        print('calculate months')
        ym = {}
        for e in d_sorted.keys():
            print(e)
            years = months = 0
            if d_sorted[e]:
                years = int( d_sorted[e] / 12 )
                months = d_sorted[e] - ( years * 12)
            ym[e] = [years, months]

        print(ym)

        context = {'formset': skillformset,
                   'skill_set': d_sorted,
                   'ym': ym
                   }
        return render(request, 'skill/edit_set_row.html', context)

    elif request.method == 'POST':
        form = SkillModelFormSet(request.POST, request.FILES, form_kwargs={'user': request.user})
        print(f'form.is_bound1 = {form.is_bound}')
        print(f'form.has_changed() = {form.has_changed()}')
        print(f'form.is_valid() = {form.is_valid()}')
        if form.is_valid():
            instances = form.save(commit=False)
            i = 0
            for instance in instances:
                i += 1
                instance.user = request.user
                instance.save()

            if form.has_changed():
                messages.success(request, f'The {i} post(s) have been successfully saved.')
                return redirect('skill:skill')
            else:
                messages.success(request, f'No changes made.')
                return redirect('skill:skill')

        else:
            for error in form.errors:
                print(error)
        
            messages.error(request, 'Please correct the following errors:')
            context = {'formset': form}
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
    skills = Skill.objects.filter(user=request.user)
    context = {'skills':  skills }
    return render(request,'skill/view.html', context)


def add_skills(d, skill, years, months):
    if skill:
        skill = skill.lower()
        if skill not in d:
            d[skill] = 0
        d[skill] += years * 12 + months
    return d



def add(request):
    if request.method == 'POST':
        print('182')

    context = {'form': SkillForm(user=request.user)}
    return render(request, 'partials/form.html', context)

def hx_delete(request, id):
    print(request.method)
    queryset = Skill.objects.filter(user=request.user)
    skill = get_object_or_404(queryset, pk=id)
    skill.delete()
    messages.success(request,  f'Skill id={id} has been deleted successfully.')
    return HttpResponse('')


# @require_http_methods(['DELETE'])
def hx(request):
    # Task.objects.filter(id=id).delete()
    # tasks = Task.objects.all()
    print(request.htmx)
    return render(request, 'skill/hx.html', {'tasks': ''})

# @csrf_protect
def hx2(request):
    return HttpResponse('hx2')



@login_required
def delete(request, id):
    pass



def hx_put(request, id):
    print('hx_put')
    print(f'request.method = {request.method}')
    # queryset = Skill.objects.filter(user=request.user)
    # i = get_object_or_404(queryset, pk=id)

    if request.method == 'PUT':
        # print('189')
        skill_put = QueryDict(request.body).dict()
        experience_id = skill_put['form-1-experience']
        skill = skill_put['form-1-skill']
        skill_years = skill_put['form-1-skill_years']
        skill_months = skill_put['form-1-skill_months']
        e = Experience.objects.get(id=experience_id)
        i = Skill.objects.get(id=id)
        i.experience = e
        i.skill = skill
        i.skill_years = skill_years
        i.skill_months = skill_months
        print(i)
        i.save()
        messages.success(request, 'The post has been updated successfully.')
        return HttpResponse('')



        #     if form.has_changed():
        #         messages.success(request, f'The post has been successfully upated.')
        #         return redirect('skill:skill')
        #     else:
        #         messages.success(request, f'No changes made.')
        #         return redirect('skill:skill')

        # context = {'form': SkillForm(user=request.user)}
        # return render(request, 'partials/form.html', context)

        # queryset = Skill.objects.filter(user=request.user)
        # skill = get_object_or_404(queryset, pk=id)

        # skill.delete()
        # messages.success(request,  f'Skill id={id} has been deleted successfully.')
        # return HttpResponse('')







@login_required
def hx_post(request, id):
    queryset = Skill.objects.filter(user=request.user)
    skills = get_object_or_404(queryset, pk=id)

    if request.method == 'GET':
        context = {'form': SkillForm(instance=skills, user=request.user), 'id': id}
        return render(request,'skill/add_edit.html', context)
    
    elif request.method == 'PUT':
        print('hx_post')
        print(f'request.method = {request.method}')
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


        else:
            messages.error(request, 'Please correct the following errors:')
            return render(request,'skill/add_edit.html', {'form':form})
