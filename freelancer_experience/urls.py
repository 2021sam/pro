# /Users/2021sam/apps/zyxe/pro/freelancer_experience/urls.py
from django.urls import path
from .views import MultiStepFormView, ExperienceList

app_name = 'freelancer_experience'

urlpatterns = [
    path('multi-step/<int:step>/', MultiStepFormView.as_view(), name='multi-step'),
    path('list/', ExperienceList.as_view(), name='experience-list'),  # Your view for listing all experiences
]



# from django.urls import path
# from . import views

# app_name = 'pro_experience'  # Namespace for the app

# urlpatterns = [
#     path('', views.view, name='experience-view'),  # List all experiences
#     path('multi-step/<int:step>/', views.MultiStepFormView.as_view(), name='multi-step'),  # Multi-step form view
#     path('delete/<int:experience_id>/', views.delete, name='experience-delete'),  # Delete an experience
# ]
