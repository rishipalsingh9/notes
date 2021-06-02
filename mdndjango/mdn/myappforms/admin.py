from django.contrib import admin
from . models import *
# Register your models here.


@admin.register(Agents)
class AgentsAdmin(admin.ModelAdmin):
    list_display = ('agency_name', 'prop_name', 'email_agent', 'agency_address', 'contact_no', 'city', 'country')

