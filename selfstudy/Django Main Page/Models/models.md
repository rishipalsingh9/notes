# MODELS

A model is the single, definitive source of information about your data. It contains the essential fields and behaviors of the data you’re storing. Generally, each model maps to a single database table.

The basics:

- Each model is a Python class that subclasses django.db.models.Model.
- Each attribute of the model represents a database field.
- With all of this, Django gives you an automatically-generated database-access API; see [Making queries](https://docs.djangoproject.com/en/3.2/topics/db/queries/).

## Quick example

This example model defines a Person, which has a first_name and last_name:

    from django.db import models

    class Person(models.Model):
        first_name = models.CharField(max_length=30)
        last_name = models.CharField(max_length=30)

first_name and last_name are fields of the model. Each field is specified as a class attribute, and each attribute maps to a database column.

The above Person model would create a database table like this:

    CREATE TABLE myapp_person (
        "id" serial NOT NULL PRIMARY KEY,
        "first_name" varchar(30) NOT NULL,
        "last_name" varchar(30) NOT NULL
    );

Some technical notes:

- The name of the table, myapp_person, is automatically derived from some model metadata but can be overridden. See Table names for more details.
- An id field is added automatically, but this behavior can be overridden. See Automatic primary key fields.
- The CREATE TABLE SQL in this example is formatted using PostgreSQL syntax, but it’s worth noting Django uses SQL tailored to the database backend specified in your settings file.

## Using Models

Once you have defined your models, you need to tell Django you’re going to use those models. Do this by editing your settings file and changing the INSTALLED_APPS setting to add the name of the module that contains your models.py.

For example, if the models for your application live in the module myapp.models (the package structure that is created for an application by the manage.py startapp script), INSTALLED_APPS should read, in part:

    INSTALLED_APPS = [
        #...
        'myapp',
        #...
    ]

When you add new apps to INSTALLED_APPS, be sure to run manage.py migrate, optionally making migrations for them first with manage.py makemigrations.

## Fields

The most important part of a model – and the only required part of a model – is the list of database fields it defines. Fields are specified by class attributes. Be careful not to choose field names that conflict with the models API like clean, save, or delete.

Example:

    from django.db import models

    class Musician(models.Model):
        first_name = models.CharField(max_length=50)
        last_name = models.CharField(max_length=50)
        instrument = models.CharField(max_length=100)

    class Album(models.Model):
        artist = models.ForeignKey(Musician, on_delete=models.CASCADE)
        name = models.CharField(max_length=100)
        release_date = models.DateField()
        num_stars = models.IntegerField()

## Field Types

Each field in your model should be an instance of the appropriate Field class. Django uses the field class types to determine a few things:

The column type, which tells the database what kind of data to store (e.g. INTEGER, VARCHAR, TEXT).
The default HTML widget to use when rendering a form field (e.g. `<input type="text">, <select>`).
The minimal validation requirements, used in Django’s admin and in automatically-generated forms.
Django ships with dozens of built-in field types; you can find the complete list in the model field reference. You can easily write your own fields if Django’s built-in ones don’t do the trick; see [Writing custom model fields](https://docs.djangoproject.com/en/3.2/howto/custom-model-fields/).

## Field Options

Each field takes a certain set of field-specific arguments (documented in the model field reference). For example, CharField (and its subclasses) require a max_length argument which specifies the size of the VARCHAR database field used to store the data.

There’s also a set of common arguments available to all field types. All are optional. They’re fully explained in the reference, but here’s a quick summary of the most often-used ones:

- null: If True, Django will store empty values as NULL in the database. Default is False.
- blank: If True, the field is allowed to be blank. Default is False.

Note that this is different than null. null is purely database-related, whereas blank is validation-related. If a field has blank=True, form validation will allow entry of an empty value. If a field has blank=False, the field will be required.

- choices: A sequence of 2-tuples to use as choices for this field. If this is given, the default form widget will be a select box instead of the standard text field and will limit choices to the choices given.

A choices list looks like this:

    YEAR_IN_SCHOOL_CHOICES = [
        ('FR', 'Freshman'),
        ('SO', 'Sophomore'),
        ('JR', 'Junior'),
        ('SR', 'Senior'),
        ('GR', 'Graduate'),
    ]

>**Note**:
A new migration is created each time the order of choices changes.

The first element in each tuple is the value that will be stored in the database. The second element is displayed by the field’s form widget.

Given a model instance, the display value for a field with choices can be accessed using the get_FOO_display() method. For example:

    from django.db import models

    class Person(models.Model):
        SHIRT_SIZES = (
            ('S', 'Small'),
            ('M', 'Medium'),
            ('L', 'Large'),
        )
        name = models.CharField(max_length=60)
        shirt_size = models.CharField(max_length=1, choices=SHIRT_SIZES)
    >>> p = Person(name="Fred Flintstone", shirt_size="L")
    >>> p.save()
    >>> p.shirt_size
    'L'
    >>> p.get_shirt_size_display()
    'Large'

You can also use enumeration classes to define choices in a concise way:

    from django.db import models

    class Runner(models.Model):
        MedalType = models.TextChoices('MedalType', 'GOLD SILVER BRONZE')
        name = models.CharField(max_length=60)
        medal = models.CharField(blank=True, choices=MedalType.choices, max_length=10)

Further examples are available in the model field reference.

- default: The default value for the field. This can be a value or a callable object. If callable it will be called every time a new object is created.
- help_text: Extra “help” text to be displayed with the form widget. It’s useful for documentation even if your field isn’t used on a form.
- primary_key: If True, this field is the primary key for the model.

If you don’t specify primary_key=True for any fields in your model, Django will automatically add an IntegerField to hold the primary key, so you don’t need to set primary_key=True on any of your fields unless you want to override the default primary-key behavior. For more, see Automatic primary key fields.

The primary key field is read-only. If you change the value of the primary key on an existing object and then save it, a new object will be created alongside the old one. For example:

    from django.db import models

    class Fruit(models.Model):
        name = models.CharField(max_length=100, primary_key=True)
    >>> fruit = Fruit.objects.create(name='Apple')
    >>> fruit.name = 'Pear'
    >>> fruit.save()
    >>> Fruit.objects.values_list('name', flat=True)
    <QuerySet ['Apple', 'Pear']>

- unique:
If True, this field must be unique throughout the table.

Again, these are just short descriptions of the most common field options. Full details can be found in the common model field option reference.

## Automatic Primary Key Fields

By default, Django gives each model an auto-incrementing primary key with the type specified per app in AppConfig.default_auto_field or globally in the DEFAULT_AUTO_FIELD setting. For example:

id = models.BigAutoField(primary_key=True)
If you’d like to specify a custom primary key, specify primary_key=True on one of your fields. If Django sees you’ve explicitly set Field.primary_key, it won’t add the automatic id column.

Each model requires exactly one field to have primary_key=True (either explicitly declared or automatically added).

>***Changed in Django 3.2:***
In older versions, auto-created primary key fields were always AutoFields.

## Verbose Field Names

Each field type, except for ForeignKey, ManyToManyField and OneToOneField, takes an optional first positional argument – a verbose name. If the verbose name isn’t given, Django will automatically create it using the field’s attribute name, converting underscores to spaces.

In this example, the verbose name is "person's first name":

    first_name = models.CharField("person's first name", max_length=30)

In this example, the verbose name is "first name":

    first_name = models.CharField(max_length=30)

ForeignKey, ManyToManyField and OneToOneField require the first argument to be a model class, so use the verbose_name keyword argument:

    poll = models.ForeignKey(
        Poll,
        on_delete=models.CASCADE,
        verbose_name="the related poll",
    )
    sites = models.ManyToManyField(Site, verbose_name="list of sites")
    place = models.OneToOneField(
        Place,
        on_delete=models.CASCADE,
        verbose_name="related place",
    )

The convention is not to capitalize the first letter of the verbose_name. Django will automatically capitalize the first letter where it needs to.

## Relationships

Clearly, the power of relational databases lies in relating tables to each other. Django offers ways to define the three most common types of database relationships: many-to-one, many-to-many and one-to-one.

### Many-To-One Relationships

To define a many-to-one relationship, use django.db.models.ForeignKey. You use it just like any other Field type: by including it as a class attribute of your model.

ForeignKey requires a positional argument: the class to which the model is related.

For example, if a Car model has a Manufacturer – that is, a Manufacturer makes multiple cars but each Car only has one Manufacturer – use the following definitions:

    from django.db import models

    class Manufacturer(models.Model):
        # ...
        pass

    class Car(models.Model):
        manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
        # ...

You can also create recursive relationships (an object with a many-to-one relationship to itself) and relationships to models not yet defined; see the model field reference for details.

It’s suggested, but not required, that the name of a ForeignKey field (manufacturer in the example above) be the name of the model, lowercase. You can call the field whatever you want. For example:

    class Car(models.Model):
        company_that_makes_it = models.ForeignKey(
            Manufacturer,
            on_delete=models.CASCADE,
        )
        # ...

>*See also*:
ForeignKey fields accept a number of extra arguments which are explained in the model field reference. These options help define how the relationship should work; all are optional.
For details on accessing backwards-related objects, see the Following relationships backward example.
For sample code, see the Many-to-one relationship model example.

### Many-To-Many Relationships

To define a many-to-many relationship, use ManyToManyField. You use it just like any other Field type: by including it as a class attribute of your model.

ManyToManyField requires a positional argument: the class to which the model is related.

For example, if a Pizza has multiple Topping objects – that is, a Topping can be on multiple pizzas and each Pizza has multiple toppings – here’s how you’d represent that:

    from django.db import models

    class Topping(models.Model):
        # ...
        pass

    class Pizza(models.Model):
        # ...
        toppings = models.ManyToManyField(Topping)

As with ForeignKey, you can also create recursive relationships (an object with a many-to-many relationship to itself) and relationships to models not yet defined.

It’s suggested, but not required, that the name of a ManyToManyField (toppings in the example above) be a plural describing the set of related model objects.

It doesn’t matter which model has the ManyToManyField, but you should only put it in one of the models – not both.

Generally, ManyToManyField instances should go in the object that’s going to be edited on a form. In the above example, toppings is in Pizza (rather than Topping having a pizzas ManyToManyField ) because it’s more natural to think about a pizza having toppings than a topping being on multiple pizzas. The way it’s set up above, the Pizza form would let users select the toppings.

>*See also*:
See the Many-to-many relationship model example for a full example.

ManyToManyField fields also accept a number of extra arguments which are explained in the model field reference. These options help define how the relationship should work; all are optional.
