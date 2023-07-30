from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='education-view'),
    path('education/add/', views.add, name='education-add'),
    # path('education/edit/<int:id>/', views.edit_education, name='education-edit')
]