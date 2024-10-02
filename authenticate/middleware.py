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
    

import logging
from django.shortcuts import redirect
from django.urls import reverse

logger = logging.getLogger(__name__)

class CheckUserSettingsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Check if the user has initialized their settings (e.g., role is None)
            if not hasattr(request.user, 'settings') or not request.user.settings.role:
                # Prevent redirect loop by checking if the user is already on the initialize-settings page
                if request.path != reverse('initialize_settings'):
                    logger.debug("User has no role, redirecting to initialize settings.")
                    return redirect('initialize_settings')
                else:
                    logger.debug("Already on the settings page.")
            else:
                logger.debug(f"User {request.user.username} has initialized settings.")
        
        # Proceed with the normal response
        response = self.get_response(request)
        return response
