from django.db import models


# Create your models here.
class Packages(models.Model):
    tour_name = models.CharField(max_length=200)
    no_of_nights = models.PositiveSmallIntegerField()
    travel_date = models.DateField()
    end_date = models.DateField()
    detail_itinerary = models.FileField(blank=True)


class Agents(models.Model):
    agency_name = models.CharField(max_length=200)
    prop_name = models.CharField(max_length=200)
    email_agent = models.EmailField()
    agency_address = models.CharField(max_length=500)
    contact_no = models.PositiveSmallIntegerField()
    city = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
