from django.db import models
from django.forms import ModelForm
from django.core import validators
#from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

#TITLE_CHOICES = [
#    ('India'),
#    ('Sri Lanka'),
#    ('Pakistan'),
#    ('Australia'),
#]

class Agent(models.Model):
    COUNTRY_CHOICES = (
        ('IND', 'India'),
        ('UK', 'United Kingdom'),
        ('BAN', 'Bangladesh'),
        ('PAK', 'Pakistan'),
        ('UAE', 'United Arab Emirates'),
    )
    agency_name = models.CharField(max_length=200)
    prop_name = models.CharField(max_length=30)
    agency_address = models.CharField(max_length=300)
    agency_city = models.CharField(max_length=50)
    agency_country = models.CharField(max_length=15, choices=COUNTRY_CHOICES)
    email_address = models.EmailField(max_length=50)
    contact_nu = models.CharField(max_length=14)

    def __str__(self):
        return self.agency_name

class AgentForm(ModelForm):
    class Meta:
        model = Agent
        fields = '__all__'
        

class Guest(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    guest_email = models.EmailField(max_length=200, default=False)
    agent = models.ForeignKey(
        Agent, on_delete=models.CASCADE, related_name='agencyname')

    def __str__(self):
        return self.first_name



class Person(models.Model):
    name = models.CharField(max_length=128)
    
    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Person, through='Membership')
    
    def __str__(self):
        return self.name

class Membership(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)
        
    def __str__(self):
        return f'{self.person} {self.group} {self.date_joined}'


class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def save(self, *args, **kwargs):
        if self.name == "Yoko Blog":
            return 'Yoko shall never have her own blog!'
        else:
            return 'file saved'
            #super(Blog, self).save(*args, **kwargs)
            
    def __str__(self):
        return f'{self.name} {self.tagline}'
    

# Abstract base class model is used to use the same fields as in all 
# other models without changing anything

class CommonInfo(models.Model):
    CODE_CHOICES = (
        ('UK', '0044'),
        ('FR', '0033'),
        ('GER', '0049'),
        ('SP', '0034'),
        ('IT', '0039'),
    )
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=208)
    city = models.CharField(max_length=20)
    country = models.CharField(max_length=30)
    country_code = models.CharField(validators = [validators.MinLengthValidator(3)], max_length=4, choices=CODE_CHOICES)
    phone_number = models.CharField(validators=[validators.MinLengthValidator(10)], max_length=10)
    email_address = models.EmailField()

    class Meta:
        abstract = True

#class Student(CommonInfo):
#    home_group = models.CharField(max_length=5)
    
#    def __str__(self):
#        return self.name

# This commoninfo type model shall be helpful to make the number of 
# models such as accommodation, attraction, day tours, etc 
# to have similar fields such as address, city, country as well as name.
