# /Users/2021sam/apps/zyxe/pro/employer_search/urls.py

from django.urls import path
from .views import SearchFreelancersByJobView, UpdateEmployerDecisionView

app_name = 'employer_search'

urlpatterns = [
    path('search/<int:job_id>/', SearchFreelancersByJobView.as_view(), name='search_freelancers_by_job'),
    path('update-decision/<int:job_id>/<int:freelancer_id>/', UpdateEmployerDecisionView.as_view(), name='update_employer_decision'),
]
