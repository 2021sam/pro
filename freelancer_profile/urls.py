# /Users/2021sam/apps/zyxe/pro/freelancer_profile/urls.py
from django.urls import path

# from employer_search.views import FreelancerDetailView
# from .views import FreelancerDetailView
from . import views

app_name = 'freelancer_profile'

urlpatterns = [
    path('multi-step/<int:step>/', views.ProfileMultiStepFormView.as_view(), name='multi-step-edit'),
    path('detail/<int:pk>/', views.FreelancerDetailView.as_view(), name='freelancer_detail'),
]
