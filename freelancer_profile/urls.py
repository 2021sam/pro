# /Users/2021sam/apps/zyxe/pro/freelancer_profile/urls.py
from django.urls import path
from . import views

app_name = 'freelancer_profile'

urlpatterns = [
    path('multi-step/<int:step>/<int:profile_id>/', views.ProfileMultiStepFormView.as_view(), name='multi-step-edit'),
]
