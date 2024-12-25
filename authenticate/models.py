# /Users/2021sam/apps/zyxe/pro/authenticate/models.py

CARRIER_CHOICES = [
    ('att', 'AT&T'),
    ('verizon', 'Verizon'),
    ('tmobile', 'T-Mobile'),
    ('sprint', 'Sprint'),
    # Add more carriers as needed
]


from django.contrib.auth.models import BaseUserManager

# Custom user manager
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field must be set")

        # Use the provided email or set it equal to the username
        if email is None:
            email = self.normalize_email(username)

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)


# Custom user model
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # No need to redefine username, it's already included in AbstractUser
    email = models.EmailField(unique=True)  # Email should still be unique and required
    mobile_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    mobile_carrier = models.CharField(max_length=10, choices=CARRIER_CHOICES, null=True, blank=True)
    mobile_authenticated = models.BooleanField(default=False)

    # Keep username as the unique identifier
    USERNAME_FIELD = 'username'  # Username remains the unique identifier for authentication
    REQUIRED_FIELDS = ['email']  # Email is required but not the unique identifier

    objects = CustomUserManager()

    def __str__(self):
        return self.username  # You can return either username or email based on preference


# models.py
from django.db import models
from django.conf import settings  # Import the custom user model

class UserSetting(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='settings')

    # Various user-specific settings
    color_theme = models.CharField(max_length=20, default='light')  # 'light' or 'dark' theme
    role = models.CharField(max_length=20, choices=[('freelancer', 'Freelancer'), ('recruiter', 'Recruiter')])
    receive_reminders = models.BooleanField(default=True)
    receive_alerts = models.BooleanField(default=True)

    # New user preferences
    font_size = models.CharField(max_length=10, choices=[('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], default='medium')
    display_density = models.CharField(max_length=11, choices=[('compact', 'Compact'), ('comfortable', 'Comfortable')], default='comfortable')
    custom_layout = models.BooleanField(default=False)
    favorites_visibility = models.BooleanField(default=True)
    high_contrast_mode = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Settings"



from django.db import models
from django.conf import settings

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    listing = models.CharField(max_length=255)  # Add this if 'listing' is supposed to be part of Favorite
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Favorite by {self.user.username} - Listing {self.listing}"
