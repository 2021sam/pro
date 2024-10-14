# /Users/2021sam/apps/zyxe/pro/freelancer_experience/urls.py


# /Users/2021sam/apps/zyxe/pro/freelancer_experience/urls.py

from django.urls import path
from .views import ExperienceList, MultiStepFormView, Home, ExperienceDeleteView

app_name = 'freelancer_experience'

urlpatterns = [
    path('', Home.as_view(), name='home'),  # Home CBV
    path('list/', ExperienceList.as_view(), name='experience-list'),  # Experience list view
    path('multi-step/<int:step>/', MultiStepFormView.as_view(), name='multi-step'),  # Multi-step form view
    path('multi-step/<int:step>/<int:experience_id>/', MultiStepFormView.as_view(), name='multi-step-edit'),
    path('delete/<int:pk>/', ExperienceDeleteView.as_view(), name='experience-delete'),  # Changed to pk
]






# from django.urls import path
# from .views import ExperienceList, MultiStepFormView, Home, ExperienceDeleteView

# app_name = 'freelancer_experience'

# urlpatterns = [
#     path('', Home.as_view(), name='home'),  # Home CBV for home page
#     path('list/', ExperienceList.as_view(), name='experience-list'),  # Experience list view
#     path('multi-step/<int:step>/', MultiStepFormView.as_view(), name='multi-step'),  # Multi-step form view
#     path('multi-step/<int:step>/<int:experience_id>/', MultiStepFormView.as_view(), name='multi-step-edit'),
#     path('delete/<int:experience_id>/', ExperienceDeleteView.as_view(), name='experience-delete'),  # Delete experience
# ]
