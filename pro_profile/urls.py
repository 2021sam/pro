from django.urls import path
from . import views


app_name='pro_profile'
urlpatterns = [
    path('edit/', views.profile_edit, name='profile-edit'),
    path('mia/', views.tool_profile_mia, name='tool-profile-mia'),
    path('delete/all/', views.tool_profile_delete_all, name='tool-profile-delete-all'),
    path('create/all/', views.tool_profile_create_all, name='tool-profile-create-all')
]
