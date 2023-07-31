from django.urls import path
from . import views

urlpatterns = [
    path('experience/', views.home, name='experience-view'),
    path('experience/add', views.create_post, name='experience-add'),
    path('experience/edit/<int:id>/', views.edit_post, name='experience-edit'),
    path('experience/delete/<int:id>/', views.delete_post, name='experience-delete'),
    # path('experience/skills/', views.skills, name='skills'),
    # path('about/', views.about, name='about')
]