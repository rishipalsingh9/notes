from django.contrib import admin

from . models import *
# Register your models here.

# Option 1 to register models is

# admin.site.register(models.Agent)


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('agency_name', 'prop_name', 'agency_address', 'agency_city', 'agency_country', 'email_address', 'contact_nu')


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'guest_email', 'agent')
    

admin.site.register(Person)
admin.site.register(Group)
admin.site.register(Membership)
admin.site.register(Blog)
#admin.site.register(Student)