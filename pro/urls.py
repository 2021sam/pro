# /Users/2021sam/apps/zyxe/pro/urls.py
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path, include
from authenticate.views import home, custom_login, custom_logout
from authenticate import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('authenticate/', include('authenticate.urls')),  # Include user app URLs
    path('accounts/login/', custom_login, name='login'),  # Override the default login view
    path('accounts/', include('django.contrib.auth.urls')),  # Include Django's built-in authentication views for the other routes
    path('logout/', custom_logout, name='logout'),
    path('', include('trailhead.urls')),
    path('pro/profile/', include('pro_profile.urls')),
    path('pro/education/', include('pro_education.urls')),
    path('pro/experience/', include('pro_experience.urls')),
    # path('pro/skills/', include('pro_skills.urls')),
    path('employer/profile/', include('employer_profile.urls', namespace='employer_profile')),
    path('employer/job/', include('employer_job.urls', namespace='employer_job')),
    path('freelancer/freelancer_experience', include('freelancer_experience.urls'))
]
