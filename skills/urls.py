from django.urls import path
from . import views


urlpatterns = [
    path('skills/', views.home, name='skills'),
    path('skills/view/', views.view, name='skills-view'),
    path('skills/view/summarize/', views.view_summarize, name='skills-summarize'),
    path('skills/add/', views.add, name='skills-add'),
    path('skills/edit/<int:id>/', views.edit, name='skills-edit'),
    path('skills/delete/<int:id>/', views.delete, name='skills-delete')
]
