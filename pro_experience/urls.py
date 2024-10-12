# /Users/2021sam/apps/zyxe/pro/pro_experience/urls.py
from django.urls import path
from . import views

app_name = 'pro_experience'  # Namespace for the app

urlpatterns = [
    path('', views.home, name='pro-experience-home'),  # Experience home view
    path('view/', views.view, name='pro-experience-list'),  # List all experiences
    path('add/', views.add_edit_experience, name='experience-add'),  # Add a new experience
    path('edit/<int:experience_id>/', views.add_edit_experience, name='experience-edit'),  # Edit an existing experience
    path('delete/<int:experience_id>/', views.delete, name='experience-delete'),  # Delete an experience
]
