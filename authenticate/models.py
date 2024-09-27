# /Users/2021sam/apps/zyxe/pro/authenticate/models.py

CARRIER_CHOICES = [
    ('att', 'AT&T'),
    ('verizon', 'Verizon'),
    ('tmobile', 'T-Mobile'),
    ('sprint', 'Sprint'),
    # Add more carriers as needed
]

# from django.contrib.auth.models import AbstractUser, BaseUserManager
# from django.db import models


# Custom user manager
from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)

        # Set username as the email if not provided
        username = extra_fields.get('username', email)

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """
        Create and return a superuser with a username and email.
        """
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
