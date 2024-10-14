# /Users/2021sam/apps/zyxe/pro/freelancer_experience/admin.py

from django.contrib import admin
from .models import FreelancerExperience, FreelancerSkill

# Register FreelancerExperience
admin.site.register(FreelancerExperience)

# Register FreelancerSkill
admin.site.register(FreelancerSkill)
