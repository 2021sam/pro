# /Users/2021sam/apps/authuser/user/models.py

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with an email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


CARRIER_CHOICES = [
    ('att', 'AT&T'),
    ('verizon', 'Verizon'),
    ('tmobile', 'T-Mobile'),
    ('sprint', 'Sprint'),
    # Add more carriers as needed
]

# Custom User Model
class CustomUser(AbstractUser):
    username = None  # Remove the default username field
    email = models.EmailField(unique=True)  # Set email field to be unique and required
    mobile_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    mobile_carrier = models.CharField(max_length=10, choices=CARRIER_CHOICES, null=True, blank=True)
    mobile_authenticated = models.BooleanField(default=False)  # For 2FA status
    # two_factor_code = models.CharField(max_length=6, null=True, blank=True)
    
    USERNAME_FIELD = 'email'  # Use email as the unique identifier for the user
    REQUIRED_FIELDS = []  # No additional required fields

    objects = CustomUserManager()  # Use CustomUserManager to manage users

    def __str__(self):
        return self.email