from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def home(request):
    context = {'user': request.user }
    return render(request,'trailhead/trailhead.html', context)
