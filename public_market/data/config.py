# config.py
from .forms import VehicleForm, VehicleDetailForm, ElectronicsForm, GenericForm
from .models import VehicleListing, ElectronicsListing, Listing

CATEGORY_CONFIG = {
    'vehicles': {
        'forms': [VehicleForm, VehicleDetailForm],
        'templates': ['vehicles/vehicle_form.html', 'vehicles/vehicle_details_form.html'],
        'model': VehicleListing,
    },
    'electronics': {
        'forms': [ElectronicsForm],
        'templates': ['electronics/electronics_form.html'],
        'model': ElectronicsListing,
    },
    # Add more categories as needed
    'default': {
        'forms': [GenericForm],
        'templates': ['generic_form.html'],
        'model': Listing,
    },
}
