from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'guest_email')


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('agency_name', 'prop_name', 'agency_address', 'agency_city', 'agency_country'
                    , 'email_address', 'contact_nu')
