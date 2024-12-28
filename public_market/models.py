# pro/public_market/models.py

from django.utils import timezone
from django.conf import settings
from django.db import models
from django.core.validators import EmailValidator, RegexValidator

class VehicleListing(models.Model):
    PINK_SLIP_CHOICES = [
        ('clean', 'Clear/Clean'),
        ('lienholder', 'Lienholder'),
        ('electronic', 'Electronic'),
        ('affidavit', 'Affidavit'),
        ('bonded', 'Bonded'),
        ('certificate_of_destruction', 'Certificate of Destruction'),
        ('flood', 'Flood/Water Damage'),
        ('junk', 'Junk'),
        ('lemon', 'Lemon'),
        ('odometer_rollback', 'Odometer Rollback'),
        ('parts_only', 'Parts Only'),
        ('rebuilt', 'Rebuilt/Reconstructed'),
        ('salvage', 'Salvage'),
        ('manufacturer_statement', "Manufacturer's Statement of Origin"),
        ('export', 'Export'),
        ('import', 'Import'),
    ]        

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=255)
    description = models.TextField()
    pink_slip_status = models.CharField(max_length=50, choices=PINK_SLIP_CHOICES, default='clear')
    year = models.PositiveIntegerField(default=None, blank=True, null=True)
    vin = models.CharField(max_length=17, unique=True, default=None, blank=True, null=True)
    make = models.CharField(max_length=255, default=None, blank=True, null=True)
    model = models.CharField(max_length=255, default=None, blank=True, null=True)
    odometer = models.PositiveIntegerField(help_text="Mileage in miles", default=None, blank=True, null=True)
    condition_choices = [
        ('new', 'New'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
    ]
    condition = models.CharField(max_length=10, choices=condition_choices, default='good')
    color = models.CharField(max_length=50, default=None, blank=True, null=True)
    repairs_needed = models.TextField(help_text="Details of repairs and costs needed to improve condition", default=None, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    zip_code = models.CharField(max_length=10, verbose_name="ZIP Code", help_text="Enter the 5 or 9 digit ZIP Code.")
    contact_email = models.EmailField(validators=[EmailValidator()], default=None, blank=True, null=True)
    contact_phone = models.CharField(max_length=20, validators=[
        RegexValidator(r'^\+?1?\d{9,15}$', 'Enter a valid phone number. Must be between 9 and 15 digits.')
    ], default=None, blank=True, null=True)
    contact_text = models.BooleanField(default=True, help_text="Can contact via text?")

    def __str__(self):
        return f"{self.year} {self.make} {self.model} ({self.condition})"



# # pro/public_market/models.py
# import os
# from django.utils.timezone import now
# from django.conf import settings
# from django.db import models

# # Function to determine upload path
# def user_post_directory_path(instance, filename):
#     return f'{instance.listing.user.id}/{instance.listing.id}/{now().strftime("%Y%m%d%H%M%S")}_{filename}'

# class VehiclePhoto(models.Model):
#     listing = models.ForeignKey(VehicleListing, related_name='photos', on_delete=models.CASCADE)
#     photo = models.ImageField(upload_to=user_post_directory_path)

#     def __str__(self):
#         return f"Photo for {self.listing.title}"
