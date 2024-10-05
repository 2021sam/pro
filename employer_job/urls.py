# /Users/2021sam/apps/zyxe/pro/employer_job/urls.py
from django.urls import path
from . import views

app_name = 'employer_job'  # This is necessary when using namespaces

urlpatterns = [
    path('', views.home, name='job'),
    path('view/', views.view, name='job-view'),
    path('add/', views.add_or_edit_job_with_skills, name='job-add'),
    path('edit/<int:id>/', views.add_or_edit_job_with_skills, name='job-edit'),
    path('delete/<int:id>/', views.delete, name='job-delete')
]
