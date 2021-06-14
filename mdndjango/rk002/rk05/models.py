from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class CommonInfo(models.Model):
    COUNTRY_CHOICES = (
        ('AU', 'Austria'),
        ('AUS', 'Australia'),
        ('BG', 'Belgium'),
        ('BAN', 'Bangladesh'),
        ('CA', 'Canada'),
        ('CR', 'Croatia'),
        ('CY', 'Cyprus'),
        ('CZ', 'Czech Republic'),
        ('DE', 'Denmark'),
        ('EG', 'Egypt'),
        ('FI', 'Finland'),
        ('FR', 'France'),
        ('GER', 'Germany'),
        ('GR', 'Greece'), 
        ('HU', 'Hungary'),
        ('ICE', 'Iceland'),
        ('IN', 'India'),
        ('IND', 'Indonesia'),
        ('IRE', 'Ireland'),
        ('IT', 'Italy'),
        ('JP', 'Japan'),
        ('LT', 'Latvia'),
        ('LUX', 'Luxembourg'),
        ('MAL', 'Malaysia'),
        ('MA', 'Maldives'),
        ('ME', 'Mexico'),
        ('MO', 'Monaco'),
        ('NT', 'Netherlands'),
        ('NZ', 'New Zealand'),
        ('NO', 'Norway'),
        ('PAK', 'Pakistan'),
        ('PL', 'Poland'),
        ('PR', 'Portugal'),
        ('RU', 'Russia'),
        ('SE', 'Seychelles'),
        ('SI', 'Singapore'),
        ('SW', 'Switzerland'),
        ('SP', 'Spain'),
        ('SR', 'Sri Lanka'),
        ('SW', 'Sweden'),
        ('SA', 'South Africa'),
        ('UR', 'Ukrain'),
        ('UAE', 'United Arab Emirates'),
        ('UK', 'United Kingdom'),
        ('US', 'United States'),
    )
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=20)
    pin_code = models.CharField(max_length=15)
    country = models.CharField(max_length=30, choices=COUNTRY_CHOICES)
    email = models.EmailField()
    
    class Meta:
        abstract = True

class Supplier(CommonInfo):
    phone = PhoneNumberField()    


class Agent(CommonInfo):
    phone = PhoneNumberField()
    

class Accommodation(CommonInfo):
    phone = PhoneNumberField()
    

class Attractions(CommonInfo):
    phone = PhoneNumberField()
    description = models.TextField(max_length=3000)


class Daytours(CommonInfo):
    phone = PhoneNumberField()
    description = models.TextField(max_length=3000)


class Tickets(CommonInfo):
    phone = PhoneNumberField()
    description = models.TextField(max_length=3000)


class Meals(CommonInfo):
    phone = PhoneNumberField()
    description = models.TextField(max_length=3000)
