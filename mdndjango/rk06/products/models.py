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
        ordering = ['name']


class Agent(CommonInfo):
    phone = PhoneNumberField()

    class Meta(CommonInfo.Meta):
        db_table = 'agent'
    # this is meta inheritance
    # db_table means that all child classes (the ones that don't specify their own Meta) would use the same db table.


class Supplier(models.Model):
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
    sup_name = models.CharField(max_length=200)
    sup_address = models.CharField(max_length=200)
    sup_city = models.CharField(max_length=20)
    sup_postal_code = models.CharField(max_length=10)
    sup_country = models.CharField(max_length=20, choices=COUNTRY_CHOICES)
    sup_email = models.EmailField()
    phone = PhoneNumberField()
    
    def __str__(self):
        return self.sup_name


class Accommodation(CommonInfo):
    phone = PhoneNumberField()
    merchant = models.ManyToManyField(Supplier, related_name="%(app_label)s_%(class)s_related",
                                        related_query_name="%(app_label)s_%(class)ss",)

# refer django 3.2.5 dev docmentation on page 100


class Attraction(CommonInfo):
    phone = PhoneNumberField()
    description = models.TextField(max_length=3000)
    merchant = models.ForeignKey(
        Supplier, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_related")


class Daytour(CommonInfo):
    phone = PhoneNumberField()
    description = models.TextField(max_length=3000)
    merchant = models.ManyToManyField(Supplier, related_name="%(app_label)s_%(class)s_related",
                                      related_query_name="%(app_label)s_%(class)ss",)


class Ticket(CommonInfo):
    phone = PhoneNumberField()
    description = models.TextField(max_length=3000)
    merchant = models.ForeignKey(
        Supplier, on_delete=models.CASCADE, related_name="provider")



class Meal(CommonInfo):
    phone = PhoneNumberField()
    description = models.TextField(max_length=3000)
    merchant = models.ForeignKey(
        Supplier, on_delete=models.CASCADE, related_name="seller")


class Transfers(models.Model):
    AIRPORT_CHOICES = (
        ('LHR', 'London Heathrow Airport'),
        ('CDG', 'Charles de Gaulle Airport Paris'),
        ('FCO', 'Leonardo da Vinci International Airport Rome'),
        ('AMS', 'Amsterdam Airport Schiphol'),
    )
    transfer_type = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=100)
    pickup_point = models.CharField(max_length=200, choices=AIRPORT_CHOICES)
    flight_no = models.CharField(max_length=30)
    pickup_date = models.DateTimeField()
    drop_point = models.CharField(max_length=100)
    merchant = models.ForeignKey(
        Supplier, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_related")
