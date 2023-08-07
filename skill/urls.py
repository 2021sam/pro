from django.urls import path
from . import views


urlpatterns = [
    path('skill/', views.home, name='skill'),
    path('skill/view/', views.view, name='skill-view'),
    path('skill/view/summarize/', views.view_summarize, name='skill-summarize'),
    path('skill/add/', views.add, name='skill-add'),
    path('skill/edit/<int:id>/', views.edit, name='skill-edit'),
    path('skill/delete/<int:id>/', views.delete, name='skill-delete')
]
