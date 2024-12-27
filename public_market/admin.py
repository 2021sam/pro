from django.contrib import admin
from .models import VehicleListing

@admin.register(VehicleListing)
class VehicleListingAdmin(admin.ModelAdmin):
    list_display = ('year', 'make', 'model', 'price', 'user', 'timestamp')
    search_fields = ('make', 'model', 'vin', 'user__username')
    list_filter = ('condition', 'pink_slip_status', 'timestamp')
