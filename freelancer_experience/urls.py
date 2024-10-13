# /Users/2021sam/apps/zyxe/freelancer_experience/urls.py
from django.urls import path
from . import views

app_name = 'freelancer_experience'

urlpatterns = [
    path('add/', views.add_experience, name='experience-add'),
    path('list/', views.view_experiences, name='experience-list'),
]
