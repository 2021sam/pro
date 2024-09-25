from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='education'),
    path('view/', views.view, name='education-view'),
    path('add/', views.add, name='education-add'),
    path('edit/<int:id>/', views.edit, name='education-edit'),
    path('delete/<int:id>/', views.delete, name='education-delete')
]