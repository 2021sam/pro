# /Users/2021sam/apps/zyxe/pro/authenticate/models.py

CARRIER_CHOICES = [
    ('att', 'AT&T'),
    ('verizon', 'Verizon'),
    ('tmobile', 'T-Mobile'),
    ('sprint', 'Sprint'),
    # Add more carriers as needed
]

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


# Custom user manager
class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field must be set")

        # Normalize the email based on the username field
        email = self.normalize_email(username)  # Set email equal to username

        # Remove email from extra_fields to avoid passing it twice
        extra_fields.pop('email', None)

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, password, **extra_fields)


# Custom user model
class CustomUser(AbstractUser):
    # Keep the username field from AbstractUser
    username = models.CharField(max_length=150, unique=True)

    # Email will be set equal to the username field
    email = models.EmailField(unique=True)  # Email is still required and unique

    mobile_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    mobile_carrier = models.CharField(max_length=10, choices=CARRIER_CHOICES, null=True, blank=True)
    mobile_authenticated = models.BooleanField(default=False)  # For 2FA status

    USERNAME_FIELD = 'username'  # Use username as the unique identifier for users
    REQUIRED_FIELDS = ['email']  # Email is still a required field, but username is the login field

    objects = CustomUserManager()  # Use CustomUserManager to handle user creation

    def __str__(self):
        return self.username
