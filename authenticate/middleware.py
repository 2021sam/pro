# /Users/2021sam/apps/zyxe/pro/authenticate/middleware.py

import logging
from django.shortcuts import redirect

logger = logging.getLogger(__name__)

class EmailVerificationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            logger.debug(f"Authenticated user: {request.user.email}")
            if not request.user.is_active:
                logger.debug(f"Inactive user: {request.user.email}, redirecting to verification.")
                return redirect('resend_verification')
        return self.get_response(request)
    

# middleware.py in your app
from django.shortcuts import redirect
from django.conf import settings

class CheckUserSettingsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Check if the user has initialized their settings (e.g., role is None)
            if not hasattr(request.user, 'settings') or not request.user.settings.role:
                # Redirect to the settings initialization page
                return redirect('initialize_settings')  # 'initialize_settings' is a URL where the user can set their settings

        response = self.get_response(request)
        return response
