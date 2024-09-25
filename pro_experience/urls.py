from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='experience'),
    path('view/', views.view, name='experience-view'),
    path('add/', views.add, name='experience-add'),
    path('edit/<int:id>/', views.edit, name='experience-edit'),
    path('delete/<int:id>/', views.delete, name='experience-delete')
]