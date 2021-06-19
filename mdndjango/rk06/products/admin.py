from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'address', 'city',
                    'pin_code', 'country', 'email', 'phone']


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['id', 'sup_name', 'sup_address', 'sup_city',
                    'sup_postal_code', 'sup_country', 'sup_email', 'phone']


@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'address', 'city',
                    'pin_code', 'country', 'email', 'phone']


@admin.register(Attraction)
class AttractionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'address', 'city',
                    'pin_code', 'country', 'email', 'phone', 'description']


@admin.register(Daytour)
class DaytourAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'address', 'city',
                    'pin_code', 'country', 'email', 'phone', 'description']


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'address', 'city',
                    'pin_code', 'country', 'email', 'phone', 'description']


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'address', 'city',
                    'pin_code', 'country', 'email', 'phone', 'description']


@admin.register(Transfers)
class TransfersAdmin(admin.ModelAdmin):
    list_display = ['id', 'transfer_type', 'vehicle_type', 'pickup_point', 'flight_no', 'pickup_date', 'drop_point']