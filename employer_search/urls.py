# /Users/2021sam/apps/zyxe/pro/employer_search/urls.py


# employer_search/urls.py
from django.urls import path
from . import views

app_name = 'employer_search'

from .views import SearchFreelancersByJobView

urlpatterns = [
    path('freelancer/search/<int:job_id>/', SearchFreelancersByJobView.as_view(), name='search_freelancers_by_job'),
]




# urlpatterns = [
#     # Search for freelancers by job
#     path('search/<int:job_id>/', views.search_freelancers_by_job, name='search_freelancers_by_job'),
#
#     # View freelancer profile detail
#     path('freelancer/<int:id>/', views.freelancer_profile_detail, name='freelancer_profile_detail'),
# ]
