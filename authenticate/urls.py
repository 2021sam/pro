# /Users/2021sam/apps/authuser/user/urls.py
from django.urls import path
from .views import sign_up, activate, resend_verification_email, custom_login, verify_account, waiting_for_approval, delete_account
from django.contrib.auth import views as auth_views
from .views import check_verification_status, profile, enable_2fa, disable_2fa, request_2fa_approval, verify_2fa_code, initialize_settings

urlpatterns = [
    path('register/', sign_up, name='register'),  # Registration
    path('activate/<uidb64>/<token>/', activate, name='activate'),  # Email verification
    path('resend-verification/', resend_verification_email, name='resend_verification'),  # Resend verification email
    
    # Custom login view
    path('login/', custom_login, name='login'),
    
    # Verification pages
    path('verify-account/', verify_account, name='verify_account'),  
    path('waiting-for-approval/', waiting_for_approval, name='waiting_for_approval'),  # Waiting for approval after registration
    path('check-verification-status/', check_verification_status, name='check_verification_status'),  # AJAX call to check if the user is verified
    
    # Password change functionality
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
    
    # Logout URL
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),  # Logout and redirect to home

    # Account deletion
    path('delete_account/', delete_account, name='delete_account'),  # Allow users to delete their account

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),

    # Profile page
    path('profile/', profile, name='profile'),
    path('enable-2fa/', enable_2fa, name='enable_2fa'),
    path('disable-2fa/', disable_2fa, name='disable_2fa'),

    path('request_2fa_approval/', request_2fa_approval, name='request_2fa_approval'),
    path('verify-2fa/', verify_2fa_code, name='verify_2fa'),


    path('initialize-settings/', initialize_settings, name='initialize_settings'),  # Add this line

]