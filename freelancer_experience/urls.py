# /Users/2021sam/apps/zyxe/pro/freelancer_experience/urls.py
from django.urls import path
from .views import ExperienceList, MultiStepFormView, Home  # Import HomeView

app_name = 'freelancer_experience'

urlpatterns = [
    path('', Home.as_view(), name='home'),  # HomeView CBV for home page
    path('list/', ExperienceList.as_view(), name='experience-list'),  # Experience list view
    path('multi-step/<int:step>/', MultiStepFormView.as_view(), name='multi-step'),  # Multi-step form view
]
