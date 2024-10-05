# urls.py
from django.urls import path
from . import views

app_name = 'employer_skill'  # This is necessary when using namespaces

urlpatterns = [
    path('', views.skill_list, name='emp_skill_list'),
    # path('add/', views.skill_add, name='skill_add'),
    path('add/<int:job_id>/', views.skill_add, name='skill_add'),  # Accept job_id in the URL
    path('edit/<int:pk>/', views.skill_edit, name='skill_edit'),  # Passes the ID (pk) to the view
    path('delete/<int:pk>/', views.skill_delete, name='skill_delete'),
]


# from django.urls import path
# from . import views

# app_name = 'employer_skill'

# urlpatterns = [
#     path('job/add/', views.job_add, name='job_add'),
#     path('skill/add/<int:job_id>/', views.skill_add, name='skill_add'),  # Accept job_id in the URL
#     path('skill/list/', views.skill_list, name='emp_skill_list'),
#     # Add other paths as necessary
# ]
