from django.urls import path
from . import views

urlpatterns = [
    path('education', views.home, name='education'),
    path('education/view/', views.view, name='education-view'),
    path('education/add/', views.add, name='education-add'),
    path('education/edit/<int:id>/', views.edit, name='education-edit'),
    path('education/delete/<int:id>/', views.delete, name='education-delete')
]