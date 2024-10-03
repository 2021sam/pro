# urls.py
from django.urls import path
from . import views

app_name = 'employer_skill'  # This is necessary when using namespaces

urlpatterns = [
    path('', views.skill_list, name='emp_skill_list'),
    path('add/', views.skill_add, name='skill_add'),
    path('edit/<int:pk>/', views.skill_edit, name='skill_edit'),  # Passes the ID (pk) to the view
    path('delete/<int:pk>/', views.skill_delete, name='skill_delete'),
]
