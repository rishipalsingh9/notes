from django.core import validators
from django import forms
from .models import Packages, Agents


class TourPackages(forms.ModelForm):
    class Meta:
        model = Packages
        fields = ['tour_name', 'no_of_nights', 'travel_date', 'end_date', 'detail_itinerary']
        labels = {'tour_name': 'Package Name', 'no_of_nights': 'No. of Nights', 'travel_date': 'Start Date',
                  'end_date': 'Tour End Date'}


class CreateAgents(forms.ModelForm):
    agency_name = forms.CharField(max_length=40, required=False)
    class Meta:
        model = Agents
        fields = ['agency_name', 'prop_name', 'email_agent', 'agency_address', 'contact_no', 'city', 'country']
        labels = {
            'agency_name': 'Agency', 'prop_name': 'Agent Name', 'agency_address': 'Address', 'city': 'City',
            'country': 'Country', 'email_agent': 'Email Add:', 'contact_no': 'Phone'
        }
