import logging
from django.shortcuts import redirect
from django.urls import reverse

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


class CheckUserSettingsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/'):  # Exclude admin paths
            return self.get_response(request)

        if request.user.is_authenticated:
            if not hasattr(request.user, 'settings') or not request.user.settings.role:
                if request.path != reverse('initialize_settings'):
                    logger.debug(f"User {request.user.username} missing settings, redirecting.")
                    return redirect('initialize_settings')
        return self.get_response(request)


# class CustomMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#         self.public_paths = [
#             reverse('public:index'),
#             reverse('public:category_list'),
#             reverse('public:item_detail', kwargs={'item_id': 1}),  # Include item_id
#         ]


#     def __call__(self, request):
#         if any(request.path.startswith(path) for path in self.public_paths):
#             return self.get_response(request)

#         if request.user.is_authenticated and not request.user.is_active:
#             logger.debug("Redirecting inactive user to verification.")
#             return redirect('resend_verification')
        
#         return self.get_response(request)
class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        public_paths = [
            reverse('public:index'),
            reverse('public:category_list'),
            reverse('public:item_detail', kwargs={'item_id': 1}),
        ]
        if request.path in public_paths or not hasattr(request, 'user'):
            return self.get_response(request)
        if request.user.is_authenticated and not request.user.is_active:
            return redirect(reverse('resend_verification'))
        return self.get_response(request)
