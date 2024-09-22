# /Users/2021sam/apps/zyxe/pro/authenticate/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from .models import CustomUser
from .forms import RegisterForm, TwoFactorForm
from django.contrib.auth.decorators import login_required
import logging

logger = logging.getLogger(__name__)


def waiting_for_approval(request):
    logger.info("waiting_for_approval")
    user_email = request.session.get('user_email')  # Fetch email from session
    logger.info(user_email)
    if not user_email:
        return redirect('login')  # Redirect to login if no email in session
    user = CustomUser.objects.get(email=user_email)
    logger.info(user)
    return render(request, 'registration/waiting_for_approval.html', {'user': user})


# Home view
def home(request):
    logger.info('Started')
    logger.debug('***************************************** home')
    # from pro.settings import SECRET_KEY, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
    # logger.debug(SECRET_KEY)
    # logger.info(EMAIL_HOST_USER)
    # logger.info(f'EMAIL_HOST_PASSWORD: {EMAIL_HOST_PASSWORD}')

    return render(request, 'home.html')

@login_required
def profile(request):
    logger.debug('***************************************** profile')
    return render(request, 'authenticate/profile.html')


from .forms import CustomAuthenticationForm
from django.contrib.auth import authenticate
def custom_login(request):
    logger.debug("Login view accessed")
    if request.method == 'POST':
        logger.debug("POST request received")
        form = CustomAuthenticationForm(request, data=request.POST)

        if form.is_valid():
            logger.debug("Login form is valid")
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Authenticate the user using the custom backend
            user = authenticate(request, username=username, password=password)

            if user is not None:
                logger.debug(f"User {user.email} found")

                if user.is_active:
                    logger.debug(f"User {user.email} is active. Logging in.")
                    login(request, user)
                    return redirect('home')  # Redirect to the home page
                else:
                    logger.debug(f"User {user.email} is inactive. Redirecting to resend verification.")
                    # Store the email in the session for use in resend_verification
                    request.session['user_email'] = user.email
                    messages.warning(request, 'Your account is inactive. Please verify your email.')
                    # return redirect('resend_verification')  # Redirect to the verification page
                    return redirect("verify_account")  # # Redirect to the verification page
            else:
                logger.debug(f"Authentication failed for {username}")
                messages.error(request, 'Invalid email or password.')
        else:
            logger.debug("Login form is invalid")
            logger.debug(f"Form errors: {form.errors}")
            messages.error(request, 'Please correct the errors below.')
    else:
        logger.debug("GET request received, rendering login form")
        form = CustomAuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})


from django.core.mail import EmailMessage

def send_verification_email(request, user):
    # Generate token and UID
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    # Build the absolute URL for email verification
    verification_url = request.build_absolute_uri(
        f"/authenticate/activate/{uid}/{token}/"
    )

    # Render the email using the new HTML template
    subject = 'Verify your email address'
    message = render_to_string('emails/new_verification_email.html', {
        'user': user,
        'verification_url': verification_url,
    })

    # Create the email
    email = EmailMessage(
        subject,
        message,
        'no-reply@zyxe.biz',  # Replace with your email
        [user.email],
    )
    
    # Ensure email is sent as HTML
    email.content_subtype = "html"

    # Send the email
    email.send(fail_silently=False)


# No need for login_required since we're handling inactive users
def resend_verification_email(request):
    # Get the user's email from the session
    user_email = request.session.get('user_email', None)
    logger.info(f'resend_verification_email: user_email: {user_email}')

    if user_email:
        try:
            # Fetch the user from the database using the email
            user = CustomUser.objects.get(email=user_email)
            if not user.is_active:
                # Logic to send the verification email
                send_verification_email(request, user)
                messages.success(request, 'A new verification email has been sent to your email address.')
                return redirect('waiting_for_approval')  # Redirect to home after sending the email
            else:
                messages.info(request, 'Your account is already verified.')
                return redirect('home')
        except CustomUser.DoesNotExist:
            messages.error(request, 'User does not exist.')
            return redirect('login')
    else:
        return redirect('login')  # If the session does not have the email, redirect to login


def verify_account(request):
    logger.debug('***************************************** verify_account')
    user_email = request.session.get('user_email', None)
    logger.info(f'user_email: {user_email}')

    if not user_email:
        # If no email is in the session, redirect to login
        return redirect('login')

    logger.info(f'request.method == {request.method}')

    if request.method == 'POST':
        try:
            user = CustomUser.objects.get(email=user_email)
            logger.info(f'184 user: {user}')
            if not user.is_active:
                # Send the verification email
                send_verification_email(request, user)
                messages.success(request, 'A new verification email has been sent to your email address.')
                return redirect('waiting_for_approval')  # Redirect to login after sending the email
            else:
                messages.info(request, 'Your account is already verified.')
                return redirect('home')
        except CustomUser.DoesNotExist:
            messages.error(request, 'User does not exist.')
            return redirect('login')

    return render(request, 'registration/verify_account.html')


def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_verification_email(request, user)
            messages.success(request, 'A verification email has been sent to your email address.')

            request.session['user_email'] = user.email

            logger.info('********************************************')
            logger.info(f'user.email: {user.email}')

            return redirect('waiting_for_approval')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegisterForm()

    return render(request, 'authenticate/register.html', {'form': form})

from django.contrib.auth import get_backends
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()

        # Fetch the backend and pass it to the login function
        backend = get_backends()[0]  # Assuming you want to use the first backend
        user.backend = f'{backend.__module__}.{backend.__class__.__name__}'

        # Log the user in
        login(request, user, backend=user.backend)
        messages.success(request, 'Your account has been activated successfully.')
        send_welcome_email(user)
        login(request, user)      
        return redirect('home')
    else:
        messages.error(request, 'The activation link is invalid or has expired.')
        return redirect('waiting_for_approval')


from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import RegisterForm
from .models import CustomUser

def send_welcome_email(user):
    # Prepare the email context (user info)
    subject = 'Welcome to Our Platform!'
    from_email = 'no-reply@zyxe.biz'
    to_email = [user.email]
    
    # Render the email template
    message = render_to_string('emails/welcome_email.html', {'user': user})
    
    # Create the email
    email = EmailMessage(subject, message, from_email, to_email)
    email.content_subtype = 'html'  # To send as HTML email
    
    # Send the email
    email.send(fail_silently=False)


from django.contrib.auth import logout

def custom_logout(request):
    logout(request)  # Logs the user out and clears the session
    return redirect('home')  # Redirects to home




from django.http import JsonResponse
from .models import CustomUser

def check_verification_status(request):
    # Assuming the user is logged in or the user email is stored in the session
    user_email = request.session.get('user_email', None)
    logger.info('************************************')
    logger.info('check_verification_status')
    if user_email:
        try:
            user = CustomUser.objects.get(email=user_email)
            # Return the verification status
            return JsonResponse({'is_active': user.is_active})
        except CustomUser.DoesNotExist:
            return JsonResponse({'is_active': False})
    else:
        return JsonResponse({'is_active': False})


# views.py (in the user app)
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

@login_required
def delete_account(request):
    if request.method == 'POST':
        # Delete the authenticated user's account
        user = request.user
        user.delete()
        messages.success(request, 'Your account has been deleted successfully.')
        return redirect('home')  # Redirect to home or any other page after deletion

    return render(request, 'authenticate/delete_account.html')


# Add this to your views.py (or ensure you are using a context processor that provides it)
# from django.conf import settings

def custom_password_reset_view(request):
    context = {
        'site_title': 'Your Site Title',  # Or dynamically get it from settings
    }
    # return render(request, 'registration/password_reset_form.html', context)
    return render(request, 'password_reset_form.html', {'name': 'YourName'})


from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ProfileForm
from .models import CustomUser

def profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            if form.cleaned_data['mobile_number'] != user.mobile_number or form.cleaned_data['mobile_carrier'] != user.mobile_carrier:
                # Reset 2FA if mobile number or carrier is changed
                user.mobile_authenticated = False
                user.is_2fa_enabled = False
                messages.warning(request, "2FA has been disabled due to changes in your mobile number or carrier. Please re-enable 2FA.")
            
            user = form.save()
            user.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=user)

    return render(request, 'authenticate/profile.html', {'form': form})

def enable_2fa(request):
    user = request.user
    if user.mobile_number and user.mobile_carrier:
        user.is_2fa_enabled = True
        user.save()
        # Simulate sending 2FA SMS here (Email-to-SMS logic)
        messages.success(request, "2FA enabled and verification sent!")
    else:
        messages.error(request, "Please complete your profile to enable 2FA.")
    return redirect('profile')

def disable_2fa(request):
    user = request.user
    user.is_2fa_enabled = False
    user.save()
    messages.success(request, "2FA disabled.")
    return redirect('profile')


def send_2fa_code(user, code):
    carrier_email_domains = {
        "verizon": "@vtext.com",
        "att": "@txt.att.net",
        "tmobile": "@tmomail.net",
        "sprint": "@messaging.sprintpcs.com",
    }

    logger.info('******************** 3')
    logger.info(user.mobile_carrier)
    if user.mobile_carrier in carrier_email_domains:
        logger.info('******************** 4')
        sms_address = f"{user.mobile_number}{carrier_email_domains[user.mobile_carrier]}"
        subject = 'ZYXE 2FA Code'
        message = f'Your two-factor authentication code is {code}.'
        send_mail(subject, message, 'no-reply@zyxe.biz', [sms_address])





from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfileForm

@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('profile')
    else:
        form = ProfileForm(instance=user)

    return render(request, 'authenticate/profile.html', {'form': form, 'user': user})


from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from .models import CustomUser
import random


@login_required
def request_2fa_approval(request):
    user = request.user
    logger.info('Requesting 2FA approval')

    if user.mobile_number and user.mobile_carrier:
        code = random.randint(100000, 999999)
        send_2fa_code(user, code)  # Send 2FA code via SMS

        # user.two_factor_code = code  # Save the code for later verification
        # user.save()

        request.session['two_factor_code'] = str(code)  # Store in session

        messages.success(request, f"A code has been sent to {user.mobile_number}.")
        return redirect('verify_2fa')  # Redirect to the 2FA verification page
    else:
        messages.error(request, "Please provide a valid mobile number and carrier.")
    
    return redirect('profile')



@login_required
def verify_2fa_code(request):
    if request.method == 'POST':
        entered_code = request.POST.get('two_factor_code')
        session_code = request.session.get('two_factor_code')

        if entered_code == session_code:
            request.user.mobile_authenticated = True
            request.user.save()
            del request.session['two_factor_code']  # Clear the session
            messages.success(request, "Two-factor authentication successful!")
            return redirect('profile')
        else:
            messages.error(request, "Invalid 2FA code. Please try again.")
            return redirect('verify_2fa')

    return render(request, 'authenticate/verify_2fa.html')