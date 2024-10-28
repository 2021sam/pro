# /Users/2021sam/apps/zyxe/pro/employer_search/urls.py

from django.urls import path
from .views import SearchFreelancersByJobView

app_name = 'employer_search'

urlpatterns = [
    path('search/<int:job_id>/', SearchFreelancersByJobView.as_view(), name='search_freelancers_by_job'),
]
