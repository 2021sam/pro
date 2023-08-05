from django.urls import path
from . import views


app_name='pro_file'
urlpatterns = [
    path('edit/', views.profile_edit, name='edit'),
    path('tool/profile/delete/all/', views.tool_profile_delete_all, name='tool-profile-delete-all'),
    path('tool/profile/create/all/', views.tool_profile_create_all, name='tool-profile-create-all')
]
