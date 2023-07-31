from django.urls import path
from . import views

urlpatterns = [
    path('experience/', views.home, name='experience'),
    path('experience/view', views.view, name='experience-view'),
    path('experience/add', views.add, name='experience-add'),
    path('experience/edit/<int:id>/', views.edit, name='experience-edit'),
    path('experience/delete/<int:id>/', views.delete, name='experience-delete'),
    # path('experience/skills/', views.skills, name='skills'),
    # path('about/', views.about, name='about')
]