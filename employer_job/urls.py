# /Users/2021sam/apps/zyxe/pro/employer_job/urls.py
from django.urls import path
from . import views

app_name = 'employer_job'  # This is necessary when using namespaces

urlpatterns = [
    path('', views.home, name='job'),
    path('view/', views.view, name='job-view'),
    path('add/', views.add_edit_job_with_skills, name='job-add'),
    path('edit/<int:job_id>/', views.add_edit_job_with_skills, name='job-edit'),  # Use job_id to match view
    path('delete/<int:job_id>/', views.delete, name='job-delete')  # Use job_id to match view
]
