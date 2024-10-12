# /Users/2021sam/apps/zyxe/pro/pro_experience/urls.py
from django.urls import path
from . import views

app_name = 'pro_experience'  # Namespace for the app

urlpatterns = [
    path('', views.home, name='experience-home'),  # Experience home view
    path('view/', views.view, name='experience-view'),  # List all experiences
    path('add/', views.add_edit_experience, name='experience-add'),  # Add a new experience
    path('edit/<int:experience_id>/', views.add_edit_experience, name='experience-edit'),  # Edit an existing experience
    path('delete/<int:experience_id>/', views.delete, name='experience-delete'),  # Delete an experience
]










# /Users/2021sam/apps/zyxe/pro/pro_skills/urls.py
# from django.urls import path
# from . import views

# app_name = 'pro_skills'  # Namespace for the app

# urlpatterns = [
#     path('', views.home, name='skill-home'),  # Skill home view
#     path('view/', views.view, name='skill-view'),  # List all skills
#     path('add/', views.add_edit_skill, name='skill-add'),  # Add a new skill
#     path('edit/<int:skill_id>/', views.add_edit_skill, name='skill-edit'),  # Edit an existing skill
#     path('delete/<int:skill_id>/', views.delete, name='skill-delete'),  # Delete a skill
# ]





# from django.urls import path
# from . import views

# app_name = 'pro_experience'  # This is necessary when using namespaces

# urlpatterns = [
#     path('', views.home, name='experience-home'),  # Home view for experiences
#     path('view/', views.view, name='experience-view'),  # View list of experiences
#     path('add/', views.add_edit_experience_with_skills, name='experience-add'),  # Add a new experience with skills
#     path('edit/<int:experience_id>/', views.add_edit_experience_with_skills, name='experience-edit'),  # Edit an existing experience
#     path('delete/<int:experience_id>/', views.delete, name='experience-delete'),  # Delete an experience
# ]
