from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('trailhead.urls')),
    path('', include('users.urls')),
    path('', include('pro_file.urls')),
    path('', include('education.urls')),
    path('', include('experience.urls')),
    path('', include('skill.urls'))
]
