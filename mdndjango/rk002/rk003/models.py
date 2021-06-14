from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class Agent(models.Model):
    agency_name = models.CharField(max_length=200)
    prop_name = models.CharField(max_length=30)
    agency_address = models.CharField(max_length=300)
    agency_city = models.CharField(max_length=50)
    agency_country = models.CharField(max_length=50)
    email_address = models.EmailField(max_length=50)
    contact_nu = models.CharField(max_length=15)

    def __str__(self):
        return self.agency_name


class Guest(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    guest_email = models.EmailField(max_length=200, default=False)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='agencyname')

    def __str__(self):
        return self.first_name


class Supplier(models.Model):
    supp_name = models.CharField(max_length=200)
    supp_address = models.CharField(max_length=200)
    supp_city = models.CharField(max_length=100)
    supp_email = models.EmailField()


class Hotel(models.Model):
    name = models.CharField(max_length=200)
    hotel_address = models.CharField(max_length=200)
    hotel_city = models.CharField(max_length=100)
    hotel_email = models.EmailField()
    supplied_by = models.ManyToManyField(Supplier)
