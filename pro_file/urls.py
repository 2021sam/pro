from django.urls import path
from . import views


app_name='pro_file'
urlpatterns = [
    path('edit/', views.profile_edit, name='edit'),
]