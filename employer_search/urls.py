# /Users/2021sam/apps/zyxe/pro/employer_search/urls.py

from django.urls import path
from . import views

app_name = 'employer_search'

urlpatterns = [
    # URL for the search form where recruiters can input job zip code and search for freelancers
    path('search/', views.search_freelancers, name='search_freelancers'),

    # URL for viewing the search results
    path('results/', views.search_results, name='search_results'),
]
