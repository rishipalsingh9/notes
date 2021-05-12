# Django Tutorial: The Local Library website

The first article in our practical tutorial series explains what you'll learn, and provides an overview of the "local library" example website we'll be working through and evolving in subsequent articles.

## Overview

Welcome to the MDN "Local Library" Django tutorial, in which we develop a website that might be used to manage the catalog for a local library. 

In this series of tutorial articles you will:

- Use Django's tools to create a skeleton website and application.
- Start and stop the development server.
- Create models to represent your application's data.
- Use the Django admin site to populate your site's data.
- Create views to retrieve specific data in response to different requests, and templates to render the data as HTML to be displayed in the browser.
- Create mappers to associate different URL patterns with specific views.
- Add user authorization and sessions to control site behavior and access.
- Work with forms.
- Write test code for your app.
- Use Django's security effectively.
- Deploy your application to production.

You have learned about some of these topics already, and touched briefly on others. By the end of the tutorial series you should know enough to develop simple Django apps by yourself.

## The LocalLibrary website

***
*LocalLibrary* is the name of the website that we'll create and evolve over the course of this series of tutorials. As you'd expect, the purpose of the website is to provide an online catalog for a small local library, where users can browse available books and manage their accounts.

This example has been carefully chosen because it can scale to show as much or as little detail as we need, and can be used to show off almost any Django feature. More importantly, it allows us to provide a guided path through the most important functionality in the Django web framework:

- In the first few tutorial articles we will define a simple browse-only library that library members can use to find out what books are available. This allows us to explore the operations that are common to almost every website: reading and displaying content from a database.
- As we progress, the library example naturally extends to demonstrate more advanced Django features. For example we can extend the library to allow users to reserve books, and use this to demonstrate how to use forms, and support user authentication.

Even though this is a very extensible example, it's called LocalLibrary for a reason — we're hoping to show the minimum information that will help you get up and running with Django quickly. As a result we'll store information about books, copies of books, authors and other key information. We won't however be storing information about other items a library might store, or provide the infrastructure needed to support multiple library sites or other "big library" features.

### I'm stuck, where can I get the source?

As you work through the tutorial we'll provide the appropriate code snippets for you to copy and paste at each point, and there will be other code that we hope you'll extend yourself (with some guidance).

If you get stuck, you can find the fully developed version of the website on [Github here.](https://github.com/mdn/django-locallibrary-tutorial)

## Summary

Now that you know a bit more about the LocalLibrary website and what you're going to learn, it's time to start creating a skeleton project to contain our example.

### In this module

- Django introduction
- Setting up a Django development environment
- Django Tutorial: The Local Library website
- Django Tutorial Part 2: Creating a skeleton website
- Django Tutorial Part 3: Using models
- Django Tutorial Part 4: Django admin site
- Django Tutorial Part 5: Creating our home page
- Django Tutorial Part 6: Generic list and detail views
- Django Tutorial Part 7: Sessions framework
- Django Tutorial Part 8: User authentication and permissions
- Django Tutorial Part 9: Working with forms
- Django Tutorial Part 10: Testing a Django web application
- Django Tutorial Part 11: Deploying Django to production
- Django web application security
- DIY Django mini blog

***

## Part 2: Creating a skelton website

This article shows how you can create a "skeleton" website, which you can then populate with site-specific settings, paths, models, views, and templates (we discuss these in later articles).

To get started:

1. Use the django-admin tool to generate a project folder, the basic file templates, and manage.py, which serves as your project management script. django-admin startproject(name)
2. Use manage.py to create one or more applications. py manage.py startapp(name)
3. Register the new applications to include them in the project.
4. Hook up the url/path mapper for each application.

> **Note:** A website may consist of one or more sections. For example, main site, blog, wiki, downloads area, etc. Django encourages you to develop these components as separate applications, which could then be re-used in different projects if desired.

For the Local Library website, the website and project folders are named locallibrary, and includes one application named catalog. The top-level folder structure will therefore be as follows:

    locallibrary/         # Website folder
        manage.py         # Script to run Django tools for this project (created using django-admin)
        locallibrary/     # Website/project folder (created using django-admin)
        catalog/          # Application folder (created using manage.py)

The following sections discuss the process steps in detail, and show how you can test your changes. At the end of this article, we discuss other site-wide configuration you might also do at this stage.

### Creating the Project

1. Open a command shell (or a terminal window), and make sure you are in your virtual environment. To Enter python3 -m venv venv
2. Navigate to where you want to store your Django apps (make it somewhere easy to find like inside your Documents folder), and create a folder for your new website (in this case: django_projects). Then change into your newly-created directory:

        mkdir django_projects && cd django_projects

3. Create the new project using the django-admin startproject command as shown, and then change into the project folder:

        django-admin startproject locallibrary
        cd locallibrary

The django-admin tool creates a folder/file structure as follows:

    locallibrary/
        manage.py
        locallibrary/
            __init__.py
            settings.py
            urls.py
            wsgi.py
            asgi.py

Our current working directory should look something like this:

    ../django_projects/locallibrary/

The *locallibrary* project sub-folder is the entry point for the website:

- `__init__.py` is an empty file that instructs Python to treat this directory as a Python package.
- settings.py contains all the website settings, including registering any applications we create, the location of our static files, database configuration details, etc.  
- urls.py defines the site URL-to-view mappings. While this could contain all the URL mapping code, it is more common to delegate some of the mappings to particular applications, as you'll see later.
- wsgi.py is used to help your Django application communicate with the webserver. You can treat this as boilerplate.
- asgi.py is a standard for Python asynchronous web apps and servers to communicate with each other. ASGI is the asynchronous successor to WSGI and provides a standard for both asynchronous and synchronous Python apps (whereas - WSGI provided a standard for synchronous apps only). It is backward-compatible with WSGI and supports multiple servers and application frameworks.

The manage.py script is used to create applications, work with databases, and start the development web server.

### Creating the catalog app

Next, run the following command to create the catalog application that will live inside our locallibrary project. Make sure to run this command from the same folder as your project's manage.py:

    python3 manage.py startapp catalog

The tool creates a new folder and populates it with files for the different parts of the application (shown in bold in the following example). Most of the files are named after their purpose (e.g. views should be stored in **views.py**, models in **models.py**, tests in **tests.py**, administration site configuration in **admin.py**, application registration in **apps.py**) and contain some minimal boilerplate code for working with the associated objects.

The updated project directory should now look like this:

    locallibrary/
        manage.py
        locallibrary/
        catalog/
            admin.py
            apps.py
            models.py
            tests.py
            views.py
            __init__.py
            migrations/

In addition we now have:

- A migrations folder, used to store "migrations" — files that allow you to automatically update your database as you modify your models. 
- `__init__.py` — an empty file created here so that Django/Python will recognize the folder as a Python Package and allow you to use its objects within other parts of the project.
  
> **Note:** Have you noticed what is missing from the files list above? While there is a place for your views and models, there is nowhere for you to put your url mappings, templates, and static files. We'll show you how to create them further along (these aren't needed in every website but they are needed in this example).

### Registering the catalog application

Now that the application has been created, we have to register it with the project so that it will be included when any tools are run (like adding models to the database for example). Applications are registered by adding them to the INSTALLED_APPS list in the project settings.

Open the project settings file, **django_projects/locallibrary/locallibrary/settings.py,** and find the definition for the INSTALLED_APPS list. Then add a new line at the end of the list, as shown below:

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        # Add our new application
        'catalog.apps.CatalogConfig', #This object was created for us in /catalog/apps.py
    ]

The new line specifies the application configuration object (CatalogConfig) that was generated for you in **/locallibrary/catalog/apps.py** when you created the application.

> **Note:** You'll notice that there are already a lot of other INSTALLED_APPS (and MIDDLEWARE, further down in the settings file). These enable support for the Django administration site and the functionality it uses (including sessions, authentication, etc).

### Specifying the database

This is also the point where you would normally specify the database to be used for the project. It makes sense to use the same database for development and production where possible, in order to avoid minor differences in behavior.  You can find out about the different options in Databases (Django docs).

We'll use the SQLite database for this example, because we don't expect to require a lot of concurrent access on a demonstration database, and it requires no additional work to set up! You can see how this database is configured in `settings.py`:

    SQLite DB as a default DB

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

    Postgres DB

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'postgres',
            'USER': 'postgres',
            'PASSWORD': 'Rishi@2311',
            'HOST': 'localhost',
            'PORT': 5433,
        }
    }

Because we are using SQLite, we don't need to do any further setup here. Let's move on!

### Other project settings

The settings.py file is also used for configuring a number of other settings, but at this point, you probably only want to change the TIME_ZONE — this should be made equal to a string from the standard List of tz database time zones (the TZ column in the table contains the values you want). Change your TIME_ZONE value to one of these strings appropriate for your time zone, for example:

    TIME_ZONE = 'Europe/London'

There are two other settings you won't change now, but that you should be aware of:

- **SECRET_KEY.** This is a secret key that is used as part of Django's website security strategy. If you're not protecting this code in development, you'll need to use a different code (perhaps read from an environment variable or file) when putting it into production. 
- **DEBUG.** This enables debugging logs to be displayed on error, rather than HTTP status code responses. This should be set to False in production as debug information is useful for attackers, but for now we can keep it set to True.

### Hooking up the URL mapper

The website is created with a URL mapper file (urls.py) in the project folder. While you can use this file to manage all your URL mappings, it is more usual to defer mappings to the associated application.

Open **locallibrary/locallibrary/urls.py** and note the instructional text which explains some of the ways to use the URL mapper.

    """locallibrary URL Configuration

    The `urlpatterns` list routes URLs to views. For more information please see:
        https://docs.djangoproject.com/en/3.1/topics/http/urls/
    Examples:
    Function views
        1. Add an import:  from my_app import views
        2. Add a URL to urlpatterns:  path('', views.home, name='home')
    Class-based views
        1. Add an import:  from other_app.views import Home
        2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
    Including another URLconf
        1. Import the include() function: from django.urls import include, path
        2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
    """
    from django.contrib import admin
    from django.urls import path

    urlpatterns = [
        path('admin/', admin.site.urls),
    ]

The URL mappings are managed through the urlpatterns variable, which is a Python list of path() functions. Each path() function either associates a URL pattern to a specific view, which will be displayed when the pattern is matched, or with another list of URL pattern testing code (in this second case, the pattern becomes the "base URL" for patterns defined in the target module). The urlpatterns list initially defines a single function that maps all URLs with the pattern admin/ to the module admin.site.urls , which contains the Administration application's own URL mapping definitions.

> **Note:** The route in path() is a string defining a URL pattern to match. This string might include a named variable (in angle brackets), e.g. `'catalog/<id>/'`. This pattern will match a URL like /catalog/any_chars/ and pass any_chars to the view as a string with parameter name id. We discuss path methods and route patterns further in later topics.

To add a new list item to the urlpatterns list, add the following lines to the bottom of the file. This new item includes a path() that forwards requests with the pattern catalog/ to the module catalog.urls (the file with the relative URL catalog/urls.py).

    # Use include() to add paths from the catalog application
    from django.urls import include

    urlpatterns += [
        path('catalog/', include('catalog.urls')),
    ]

> **Note:** Note that we included the import line (from django.urls import include) with the code that uses it (so it is easy to see what we've added), but it is common to include all your import lines at the top of a Python file.

Now let's redirect the root URL of our site (i.e. 127.0.0.1:8000) to the URL 127.0.0.1:8000/catalog/. This is the only app we'll be using in this project. To do this, we'll use a special view function, RedirectView, which takes the new relative URL to redirect to (/catalog/) as its first argument when the URL pattern specified in the path() function is matched (the root URL, in this case).

Add the following lines to the bottom of the file:

    #Add URL maps to redirect the base URL to our application
    from django.views.generic import RedirectView
    urlpatterns += [
        path('', RedirectView.as_view(url='catalog/', permanent=True)),
    ]

Leave the first parameter of the path function empty to imply '/'. If you write the first parameter as '/' Django will give you the following warning when you start the development server:

    System check identified some issues:

    WARNINGS:
    ?: (urls.W002) Your URL pattern '/' has a route beginning with a '/'.
    Remove this slash as it is unnecessary.
    If this pattern is targeted in an include(), ensure the include() pattern has a trailing '/'.

Django does not serve static files like CSS, JavaScript, and images by default, but it can be useful for the development web server to do so while you're creating your site. As a final addition to this URL mapper, you can enable the serving of static files during development by appending the following lines.

Add the following final block to the bottom of the file now:

    # Use static() to add url mapping to serve static files during development (only)
    from django.conf import settings
    from django.conf.urls.static import static

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

> **Note:** There are a number of ways to extend the urlpatterns list (previously, we just appended a new list item using the += operator to clearly separate the old and new code). We could have instead just included this new pattern-map in the original list definition:

    mdn/urls.py (project main url file)
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('catalog/', include('catalog.urls')),
        path('', RedirectView.as_view(url='catalog/')),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

As a final step, create a file inside your catalog folder called urls.py, and add the following text to define the (empty) imported urlpatterns. This is where we'll add our patterns as we build the application.

    from django.urls import path
    from . import views

    urlpatterns = [

    ]

### Testing the website framework

At this point we have a complete skeleton project. The website doesn't actually do anything yet, but it's worth running it to make sure that none of our changes have broken anything.

Before we do that, we should first run a database migration. This updates our database (to include any models in our installed applications) and removes some build warnings.

Running database migrations
Django uses an Object-Relational-Mapper (ORM) to map model definitions in the Django code to the data structure used by the underlying database. As we change our model definitions, Django tracks the changes and can create database migration scripts (in /locallibrary/catalog/migrations/) to automatically migrate the underlying data structure in the database to match the model.

When we created the website, Django automatically added a number of models for use by the admin section of the site (which we'll look at later). Run the following commands to define tables for those models in the database (make sure you are in the directory that contains manage.py):

    python3 manage.py makemigrations
    python3 manage.py migrate

> *Important:* You'll need to run these commands every time your models change in a way that will affect the structure of the data that needs to be stored (including both addition and removal of whole models and individual fields).

The makemigrations command creates (but does not apply) the migrations for all applications installed in your project. You can specify the application name as well to just run a migration for a single project. This gives you a chance to check out the code for these migrations before they are applied. If you're a Django expert, you may choose to tweak them slightly!

The migrate command is what applies the migrations to your database. Django tracks which ones have been added to the current database.

### Running the website

During development, you can serve the website first using the development web server, and then viewing it on your local web browser.

> **Note:** The development web server is not robust or performant enough for production use, but it is a very easy way to get your Django website up and running during development to give it a convenient quick test. By default it will serve the site to your local computer (http://127.0.0.1:8000/), but you can also specify other computers on your network to serve to. For more information see [django-admin and manage.py: runserver](https://docs.djangoproject.com/en/3.1/ref/django-admin/#runserver)

Run the development web server by calling the runserver command (in the same directory as manage.py):

### Summary

You have now created a complete skeleton website project, which you can go on to populate with urls, models, views, and templates.

Now that the skeleton for the Local Library website is complete and running, it's time to start writing the code that makes this website do what it is supposed to do.

## Part 3: Using models

***
This article shows how to define models for the LocalLibrary website. It explains what a model is, how it is declared, and some of the main field types. It also briefly shows a few of the main ways you can access model data.

### Overview

Django web applications access and manage data through Python objects referred to as models. Models define the structure of stored data, including the field types and possibly also their maximum size, default values, selection list options, help text for documentation, label text for forms, etc. The definition of the model is independent of the underlying database — you can choose one of several as part of your project settings. Once you've chosen what database you want to use, you don't need to talk to it directly at all — you just write your model structure and other code, and Django handles all the dirty work of communicating with the database for you.

This tutorial shows how to define and access the models for the LocalLibrary website example.

### Designing the LocalLibraryModels

Before you jump in and start coding the models, it's worth taking a few minutes to think about what data we need to store and the relationships between the different objects.

We know that we need to store information about books (title, summary, author, written language, category, ISBN) and that we might have multiple copies available (with globally unique id, availability status, etc.). We might need to store more information about the author than just their name, and there might be multiple authors with the same or similar names. We want to be able to sort information based on book title, author, written language, and category.

When designing your models it makes sense to have separate models for every "object" (a group of related information). In this case, the obvious objects are books, book instances, and authors.

You might also want to use models to represent selection-list options (e.g. like a drop down list of choices), rather than hard coding the choices into the website itself — this is recommended when all the options aren't known up front or may change. Obvious candidates for models, in this case, include the book genre (e.g. Science Fiction, French Poetry, etc.) and language (English, French, Japanese).

Once we've decided on our models and field, we need to think about the relationships. Django allows you to define relationships that are one to one (OneToOneField), one to many (ForeignKey) and many to many (ManyToManyField).

With that in mind, the UML association diagram below shows the models we'll define in this case (as boxes).

![Lib Model Diagram](../../static/catalog/images/libmodel.png)

We've created models for the book (the generic details of the book), book instance (status of specific physical copies of the book available in the system), and author. We have also decided to have a model for the genre so that values can be created/selected through the admin interface. We've decided not to have a model for the BookInstance:status — we've hardcoded the values (LOAN_STATUS) because we don't expect these to change. Within each of the boxes, you can see the model name, the field names, and types, and also the methods and their return types.

The diagram also shows the relationships between the models, including their multiplicities. The multiplicities are the numbers on the diagram showing the numbers (maximum and minimum) of each model that may be present in the relationship. For example, the connecting line between the boxes shows that Book and a Genre are related. The numbers close to the Genre model show that a book must have one or more Genres (as many as you like), while the numbers on the other end of the line next to the Book model show that a Genre can have zero or many associated books.

> **Note:** The next section provides a basic primer explaining how models are defined and used. As you read it, consider how we will construct each of the models in the diagram above.

### Model Primer

This section provides a brief overview of how a model is defined and some of the more important fields and field arguments.

**Model Defination** Models are usually defined in an application's models.py file. They are implemented as subclasses of django.db.models.Model, and can include fields, methods and metadata. The code fragment below shows a "typical" model, named MyModelName:

    from django.db import models

    class MyModelName(models.Model):
        """A typical class defining a model, derived from the Model class."""

        # Fields
        my_field_name = models.CharField(max_length=20, help_text='Enter field documentation')
        ...

        # Metadata
        class Meta:
            ordering = ['-my_field_name']

        # Methods
        def get_absolute_url(self):
            """Returns the url to access a particular instance of MyModelName."""
            return reverse('model-detail-view', args=[str(self.id)])

        def __str__(self):
            """String for representing the MyModelName object (in Admin site etc.)."""
            return self.my_field_name

In the below sections we'll explore each of the features inside the model in detail:

### Field

A model can have an arbitrary number of fields, of any type — each one represents a column of data that we want to store in one of our database tables. Each database record (row) will consist of one of each field value. Let's look at the example seen below:

    my_field_name = models.CharField(max_length=20, help_text='Enter field documentation')

Our above example has a single field called my_field_name, of type models.CharField — which means that this field will contain strings of alphanumeric characters. The field types are assigned using specific classes, which determine the type of record that is used to store the data in the database, along with validation criteria to be used when values are received from an HTML form (i.e. what constitutes a valid value). The field types can also take arguments that further specify how the field is stored or can be used. In this case we are giving our field two arguments:

- max_length=20 — States that the maximum length of a value in this field is 20 characters.
- help_text='Enter field documentation' — provides a text label to display to help users know what value to provide when this value is to be entered by a user via an HTML form.

The field name is used to refer to it in queries and templates. Fields also have a label specified as an argument (verbose_name), the default value of which is None, meaning replacing any underscores in the field name with a space (for example my_field_name would have a default label of my field name). Note that when the label is used as a form label through Django frame, the first letter of the label is capitalised (for example my_field_name would be My field name).

The order that fields are declared will affect their default order if a model is rendered in a form (e.g. in the Admin site), though this may be overridden.

### Common Field Arguments

The following common arguments can be used when declaring many/most of the different field types:

- help_text: Provides a text label for HTML forms (e.g. in the admin site), as described above.
- verbose_name: A human-readable name for the field used in field labels. If not specified, Django will infer the default verbose name from the field name.
- default: The default value for the field. This can be a value or a callable object, in which case the object will be called every time a new record is created.
- null: If True, Django will store blank values as NULL in the database for fields where this is appropriate (a CharField will instead store an empty string). The default is False.
- blank: If True, the field is allowed to be blank in your forms. The default is False, which means that Django's form validation will force you to enter a value. This is often used with null=True , because if you're going to allow blank values, you also want the database to be able to represent them appropriately.
- choices: A group of choices for this field. If this is provided, the default corresponding form widget will be a select box with these choices instead of the standard text field.
- primary_key: If True, sets the current field as the primary key for the model (A primary key is a special database column designated to uniquely identify all the different table records). If no field is specified as the primary key then Django will automatically add a field for this purpose.

There are many other options — you can view the [full list of field options here.](https://docs.djangoproject.com/en/3.1/ref/models/fields/#field-options)

### Common Field Types

The following list describes some of the more commonly used types of fields. 

- CharField is used to define short-to-mid sized fixed-length strings. You must specify the max_length of the data to be stored.
- TextField is used for large arbitrary-length strings. You may specify a max_length for the field, but this is used only when the field is displayed in forms (it is not enforced at the database level).
- IntegerField is a field for storing integer (whole number) values, and for validating entered values as integers in forms.
- DateField and DateTimeField are used for storing/representing dates and date/time information (as Python datetime.date in and datetime.datetime objects, respectively). These fields can additionally declare the (mutually exclusive) parameters auto_now=True (to set the field to the current date every time the model is saved), auto_now_add (to only set the date when the model is first created) , and default (to set a default date that can be overridden by the user).
- EmailField is used to store and validate email addresses.
- FileField and ImageField are used to upload files and images respectively (the ImageField adds additional validation that the uploaded file is an image). These have parameters to define how and where the uploaded files are stored.
- AutoField is a special type of IntegerField that automatically increments. A primary key of this type is automatically added to your model if you don’t explicitly specify one.
- ForeignKey is used to specify a one-to-many relationship to another database model (e.g. a car has one manufacturer, but a manufacturer can make many cars). The "one" side of the relationship is the model that contains the "key" (models containing a "foreign key" referring to that "key", are on the "many" side of such a relationship).
- ManyToManyField is used to specify a many-to-many relationship (e.g. a book can have several genres, and each genre can contain several books). In our library app we will use these very similarly to ForeignKeys, but they can be used in more complicated ways to describe the relationships between groups. These have the parameter on_delete to define what happens when the associated record is deleted (e.g. a value of models.SET_NULL would set the value to NULL).

There are many other types of fields, including fields for different types of numbers (big integers, small integers, floats), booleans, URLs, slugs, unique ids, and other "time-related" information (duration, time, etc.). You can view the [full list here.](https://docs.djangoproject.com/en/3.1/ref/models/fields/#field-types)

### Metadata

You can declare model-level metadata for your Model by declaring class Meta, as shown.

    class Meta:
        ordering = ['-my_field_name']

One of the most useful features of this metadata is to control the default ordering of records returned when you query the model type. You do this by specifying the match order in a list of field names to the ordering attribute, as shown above. The ordering will depend on the type of field (character fields are sorted alphabetically, while date fields are sorted in chronological order). As shown above, you can prefix the field name with a minus symbol (-) to reverse the sorting order.

So as an example, if we chose to sort books like this by default:

    ordering = ['title', '-pubdate']

the books would be sorted alphabetically by title, from A-Z, and then by publication date inside each title, from newest to oldest.

Another common attribute is verbose_name, a verbose name for the class in singular and plural form:

    verbose_name = 'BetterName'

Other useful attributes allow you to create and apply new "access permissions" for the model (default permissions are applied automatically), allow ordering based on another field, or to declare that the class is "abstract" (a base class that you cannot create records for, and will instead be derived from to create other models).

Many of the other metadata options control what database must be used for the model and how the data is stored (these are really only useful if you need to map a model to an existing database).

The full list of metadata options are available here: Model [metadata options](https://docs.djangoproject.com/en/3.1/ref/models/options/) (Django docs).

### Models

A model can also have methods.

Minimally, in every model you should define the standard Python class method `__str__()` to return a human-readable string for each object. This string is used to represent individual records in the administration site (and anywhere else you need to refer to a model instance). Often this will return a title or name field from the model.

    def __str__(self):
        return self.field_name

Another common method to include in Django models is get_absolute_url(), which returns a URL for displaying individual model records on the website (if you define this method then Django will automatically add a "View on Site" button to the model's record editing screens in the Admin site). A typical pattern for get_absolute_url() is shown below.

    def get_absolute_url(self):
        """Returns the url to access a particular instance of the model."""
        return reverse('model-detail-view', args=[str(self.id)])

> **Note:** Assuming you will use URLs like /myapplication/mymodelname/2 to display individual records for your model (where "2" is the id for a particular record), you will need to create a URL mapper to pass the response and id to a "model detail view" (which will do the work required to display the record). The reverse() function above is able to "reverse" your url mapper (in the above case named 'model-detail-view') in order to create a URL of the right format.
Of course to make this work you still have to write the URL mapping, view, and template!

You can also define any other methods you like, and call them from your code or templates (provided that they don't take any parameters).

### Model Management

Once you've defined your model classes you can use them to create, update, or delete records, and to run queries to get all records or particular subsets of records. We'll show you how to do that in the tutorial when we define our views, but here is a brief summary.

Creating and modifying records
To create a record you can define an instance of the model and then call save().

    # Create a new record using the model's constructor.
    record = MyModelName(my_field_name="Instance #1")

    # Save the object into the database.
    record.save()

> **Note:** If you haven't declared any field as a primary_key, the new record will be given one automatically, with the field name id. You could query this field after saving the above record, and it would have a value of 1.

You can access the fields in this new record using the dot syntax, and change the values. You have to call save() to store modified values to the database.

    # Access model field values using Python attributes.
    print(record.id) # should return 1 for the first record.
    print(record.my_field_name) # should print 'Instance #1'

    # Change record by modifying the fields, then calling save().
    record.my_field_name = "New Instance Name"
    record.save()

### Searching for Records

You can search for records that match certain criteria using the model's objects attribute (provided by the base class).

> **Note:** Explaining how to search for records using "abstract" model and field names can be a little confusing. In the discussion below we'll refer to a Book model with title and genre fields, where genre is also a model with a single field name.

We can get all records for a model as a QuerySet, using objects.all(). The QuerySet is an iterable object, meaning that it contains a number of objects that we can iterate/loop through.

    all_books = Book.objects.all()

Django's filter() method allows us to filter the returned QuerySet to match a specified text or numeric field against particular criteria. For example, to filter for books that contain "wild" in the title and then count them, we could do the following.

    wild_books = Book.objects.filter(title__contains='wild')
    number_wild_books = wild_books.count()

The fields to match and the type of match are defined in the filter parameter name, using the format: field_name__match_type (note the double underscore between title and contains above). Above we're filtering title with a case-sensitive match. There are many other types of matches you can do: icontains (case insensitive), iexact (case-insensitive exact match), exact (case-sensitive exact match) and in, gt (greater than), startswith, etc. [The full list is here](https://docs.djangoproject.com/en/3.1/ref/models/querysets/#field-lookups).

In some cases you'll need to filter on a field that defines a one-to-many relationship to another model (e.g. a ForeignKey). In this case you can "index" to fields within the related model with additional double underscores. So for example to filter for books with a specific genre pattern, you will have to index to the name through the genre field, as shown below:

    # Will match on: Fiction, Science fiction, non-fiction etc.
    books_containing_genre = Book.objects.filter(genre__name__icontains='fiction')

> **Note:** You can use underscores (__) to navigate as many levels of relationships (ForeignKey/ManyToManyField) as you like. For example, a Book that had different types, defined using a further "cover" relationship might have a parameter name: type__cover__name__exact='hard'.

There is a lot more you can do with queries, including backwards searches from related models, chaining filters, returning a smaller set of values etc. For more information see [Making queries](https://docs.djangoproject.com/en/3.1/topics/db/queries/) (Django Docs).

### Defining the LocalLibrary Models

In this section we will start defining the models for the library. Open models.py (in /locallibrary/catalog/). The boilerplate at the top of the page imports the models module, which contains the model base class models.Model that our models will inherit from.

#### Genre Model

Copy the Genre model code shown below and paste it into the bottom of your models.py file. This model is used to store information about the book category — for example whether it is fiction or non-fiction, romance or military history, etc. As mentioned above, we've created the Genre as a model rather than as free text or a selection list so that the possible values can be managed through the database rather than being hard coded.

    class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction)')

    def __str__(self):
        """String for representing the Model object."""
        return self.name

The model has a single CharField field (name), which is used to describe the genre (this is limited to 200 characters and has some help_text. At the end of the model we declare a `__str__()` method, which returns the name of the genre defined by a particular record. No verbose name has been defined, so the field will be called Name in forms.

#### Book Model

Copy the Book model below and again paste it into the bottom of your file. The Book model represents all information about an available book in a general sense, but not a particular physical "instance" or "copy" available for loan. The model uses a CharField to represent the book's title and isbn . For isbn, note how the first unnamed parameter explicitly sets the label as "ISBN" (otherwise it would default to "Isbn").  We also set parameter unique as true in order to ensure all books have a unique ISBN (the unique parameter makes the field value globally unique in a table). The model uses TextField for the summary, because this text may need to be quite long.

    catalog/models.py

    from django.urls import reverse # Used to generate URLs by reversing the URL patterns

    class Book(models.Model):
        """Model representing a book (but not a specific copy of a book)."""
        title = models.CharField(max_length=200)

        # Foreign Key used because book can only have one author, but authors can have multiple books
        # Author as a string rather than object because it hasn't been declared yet in the file
        author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

        summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
        isbn = models.CharField('ISBN', max_length=13, unique=True,
                                help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

        # ManyToManyField used because genre can contain many books. Books can cover many genres.
        # Genre class has already been defined so we can specify the object above.
        genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')

        def __str__(self):
            """String for representing the Model object."""
            return self.title

        def get_absolute_url(self):
            """Returns the url to access a detail record for this book."""
            return reverse('book-detail', args=[str(self.id)])

The genre is a ManyToManyField, so that a book can have multiple genres and a genre can have many books. The author is declared as ForeignKey, so each book will only have one author, but an author may have many books (in practice a book might have multiple authors, but not in this implementation!)

In both field types the related model class is declared as the first unnamed parameter using either the model class or a string containing the name of the related model. You must use the name of the model as a string if the associated class has not yet been defined in this file before it is referenced! The other parameters of interest in the author field are null=True, which allows the database to store a Null value if no author is selected, and on_delete=models.SET_NULL, which will set the value of the book's author field to Null if the associated author record is deleted.

> *Warning:* By default on_delete=models.CASCADE, which means that if the author was deleted, this book would be deleted too! We use SET_NULL here, but we could also use PROTECT or RESTRICT to prevent the author being deleted while any book uses it.

The model also defines `__str__()` , using the book's title field to represent a Book record. The final method, get_absolute_url() returns a URL that can be used to access a detail record for this model (for this to work we will have to define a URL mapping that has the name book-detail, and define an associated view and template).

#### BookInstance Model

Next, copy the BookInstance model (shown below) under the other models. The BookInstance represents a specific copy of a book that someone might borrow, and includes information about whether the copy is available or on what date it is expected back, "imprint" or version details, and a unique id for the book in the library.

Some of the fields and methods will now be familiar. The model uses:

- ForeignKey to identify the associated Book (each book can have many copies, but a copy can only have one Book). The key specifies on_delete=models.RESTRICT to ensure that the Book cannot be deleted while referenced by a BookInstance.
- CharField to represent the imprint (specific release) of the book.

    catalog/models.py

    import uuid # Required for unique book instances

    class BookInstance(models.Model):
        """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')
        book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
        imprint = models.CharField(max_length=200)
        due_back = models.DateField(null=True, blank=True)

        LOAN_STATUS = (
            ('m', 'Maintenance'),
            ('o', 'On loan'),
            ('a', 'Available'),
            ('r', 'Reserved'),
        )

        status = models.CharField(
            max_length=1,
            choices=LOAN_STATUS,
            blank=True,
            default='m',
            help_text='Book availability',
        )

        class Meta:
            ordering = ['due_back']

        def __str__(self):
            """String for representing the Model object."""
            return f'{self.id} ({self.book.title})'

We additionally declare a few new types of field:

- UUIDField is used for the id field to set it as the primary_key for this model. This type of field allocates a globally unique value for each instance (one for every book you can find in the library).
- DateField is used for the due_back date (at which the book is expected to become available after being borrowed or in maintenance). This value can be blank or null (needed for when the book is available). The model metadata (Class Meta) uses this field to order records when they are returned in a query.
- status is a CharField that defines a choice/selection list. As you can see, we define a tuple containing tuples of key-value pairs and pass it to the choices argument. The value in a key/value pair is a display value that a user can select, while the keys are the values that are actually saved if the option is selected. We've also set a default value of 'm' (maintenance) as books will initially be created unavailable before they are stocked on the shelves.

The method `__str__()` represents the BookInstance object using a combination of its unique id and the associated Book's title.

> **Note:** A little Python:
Starting with Python 3.6, you can use the string interpolation syntax (also known as f-strings): f'{self.id} ({self.book.title})'.
In older versions of this tutorial, we were using a formatted string syntax, which is also a valid way of formatting strings in Python (e.g. '{0} ({1})'.format(self.id,self.book.title)).

#### Author Model

Copy the Author model (shown below) underneath the existing code in models.py.

    catalog/models.py

    class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'

All of the fields/methods should now be familiar. The model defines an author as having a first name, last name, and dates of birth and death (both optional). It specifies that by default the `__str__()` returns the name in last name, firstname order. The get_absolute_url() method reverses the author-detail URL mapping to get the URL for displaying an individual author.

## Part 4: Django Admin

Now that we've created models for the LocalLibrary website, we'll use the Django Admin site to add some "real" book data. First we'll show you how to register the models with the admin site, then we'll show you how to login and create some data. At the end of the article we will show some of the ways you can further improve the presentation of the Admin site.

The Django admin application can use your models to automatically build a site area that you can use to create, view, update, and delete records. This can save you a lot of time during development, making it very easy to test your models and get a feel for whether you have the right data. The admin application can also be useful for managing data in production, depending on the type of website. The Django project recommends it only for internal data management (i.e. just for use by admins, or people internal to your organization), as the model-centric approach is not necessarily the best possible interface for all users, and exposes a lot of unnecessary detail about the models. 

All the configuration required to include the admin application in your website was done automatically when you created the skeleton project (for information about actual dependencies needed, see the Django docs here). As a result, all you must do to add your models to the admin application is to register them. At the end of this article we'll provide a brief demonstration of how you might further configure the admin area to better display our model data.

After registering the models we'll show how to create a new "superuser", login to the site, and create some books, authors, book instances, and genres. These will be useful for testing the views and templates we'll start creating in the next tutorial.

### Registering Models with Admin site

First, open admin.py in the catalog application (/locallibrary/catalog/admin.py). It currently looks like this — note that it already imports django.contrib.admin:

    catalog/admin.py

    from django.contrib import admin

    # Register your models here.

Register the models by copying the following text into the bottom of the file. This code imports the models and then calls admin.site.register to register each of them.

    from .models import Author, Genre, Book, BookInstance

    admin.site.register(Book)
    admin.site.register(Author)
    admin.site.register(Genre)
    admin.site.register(BookInstance)

> Note: If you accepted the challenge to create a model to represent the natural language of a book [(see the models tutorial article)](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Models), import and register it too!

This is the simplest way of registering a model, or models, with the site. The admin site is highly customisable, and we'll talk more about the other ways of registering your models further down.

### Creating a Superuser

In order to log into the admin site, we need a user account with Staff status enabled. In order to view and create records we also need this user to have permissions to manage all our objects.  You can create a "superuser" account that has full access to the site and all needed permissions using manage.py.

Call the following command, in the same directory as manage.py, to create the superuser. You will be prompted to enter a username, email address, and strong password.

    python3 manage.py createsuperuser

Once this command completes a new superuser will have been added to the database. Now restart the development server so we can test the login:

    python3 manage.py runserver

### Logging in and using the site

To login to the site, open the /admin URL (e.g. http://127.0.0.1:8000/admin) and enter your new superuser userid and password credentials (you'll be redirected to the login page, and then back to the /admin URL after you've entered your details).

This part of the site displays all our models, grouped by installed application. You can click on a model name to go to a screen that lists all its associated records, and you can further click on those records to edit them. You can also directly click the Add link next to each model to start creating a record of that type.

Click on the Add link to the right of Books to create a new book (this will display a dialog much like the one below). Note how the titles of each field, the type of widget used, and the help_text (if any) match the values you specified in the model. 

Enter values for the fields. You can create new authors or genres by pressing the + button next to the respective fields (or select existing values from the lists if you've already created them). When you're done you can press **SAVE, Save and add another, or Save and continue editing** to save the record.

> **Note:** At this point we'd like you to spend some time adding a few books, authors, and genres (e.g. Fantasy) to your application. Make sure that each author and genre includes a couple of different books (this will make your list and detail views more interesting when we implement them later on in the article series).

When you've finished adding books, click on the Home link in the top bookmark to be taken back to the main admin page. Then click on the Books link to display the current list of books (or on one of the other links to see other model lists). Now that you've added a few books, the list might look similar to the screenshot below. The title of each book is displayed; this is the value returned in the Book model's `__str__()` method that we specified in the last article.

From this list you can delete books by selecting the checkbox next to the book you don't want, selecting the delete... action from the Action drop-down list, and then pressing the Go button. You can also add new books by pressing the ADD BOOK button. 

You can edit a book by selecting its name in the link. The edit page for a book, shown below, is almost identical to the "Add" page. The main differences are the page title (Change book) and the addition of Delete, HISTORY and VIEW ON SITE buttons (this last button appears because we defined the get_absolute_url() method in our model).
Now navigate back to the Home page (using the Home link in the breadcrumb trail) and then view the Author and Genre lists — you should already have quite a few created from when you added the new books, but feel free to add some more.

What you won't have is any Book Instances, because these are not created from Books (although you can create a Book from a BookInstance — this is the nature of the ForeignKey field). Navigate back to the Home page and press the associated Add button to display the Add book instance screen below. Note the large, globally unique Id, which can be used to separately identify a single copy of a book in the library.

Create a number of these records for each of your books. Set the status as Available for at least some records and On loan for others. If the status is not Available, then also set a future Due back date.

That's it! You've now learned how to set up and use the administration site. You've also created records for Book, BookInstance, Genre, and Author that we'll be able to use once we create our own views and templates.

### Advanced configuration

Django does a pretty good job of creating a basic admin site using the information from the registered models:

- Each model has a list of individual records, identified by the string created with the model's `__str__()` method, and linked to detail views/forms for editing. By default, this view has an action menu at the top that you can use to perform bulk delete operations on records.
- The model detail record forms for editing and adding records contain all the fields in the model, laid out vertically in their declaration order.  

You can further customise the interface to make it even easier to use. Some of the things you can do are:

- List views:
  - Add additional fields/information displayed for each record. 
  - Add filters to select which records are listed, based on date or some other selection value (e.g. Book loan status).
  - Add additional options to the actions menu in list views and choose where this menu is displayed on the form.
- Detail views
  - Choose which fields to display (or exclude), along with their order, grouping, whether they are editable, the widget used, orientation etc.
  - Add related fields to a record to allow inline editing (e.g. add the ability to add and edit book records while you're creating their author record).

In this section we're going to look at a few changes that will improve the interface for our LocalLibrary, including adding more information to Book and Author model lists, and improving the layout of their edit views. We won't change the Language and Genre model presentation because they only have one field each, so there is no real benefit in doing so!

You can find a complete reference of all the admin site customisation choices in [The Django Admin site](https://docs.djangoproject.com/en/3.1/ref/contrib/admin/) (Django Docs).

### Register a ModelAdmin Class

To change how a model is displayed in the admin interface you define a ModelAdmin class (which describes the layout) and register it with the model.

Let's start with the Author model. Open admin.py in the catalog application (/locallibrary/catalog/admin.py). Comment out your original registration (prefix it with a #) for the Author model:

    # admin.site.register(Author)

Now add a new AuthorAdmin and registration as shown below.

    # Define the admin class
    class AuthorAdmin(admin.ModelAdmin):
        pass

    # Register the admin class with the associated model
    admin.site.register(Author, AuthorAdmin)

Now we'll add ModelAdmin classes for Book, and BookInstance. We again need to comment out the original registrations:

    # admin.site.register(Book)
    # admin.site.register(BookInstance)

Now to create and register the new models; for the purpose of this demonstration, we'll instead use the @register decorator to register the models (this does exactly the same thing as the admin.site.register() syntax):

    # Register the Admin classes for Book using the decorator
    @admin.register(Book)
    class BookAdmin(admin.ModelAdmin):
        pass

    # Register the Admin classes for BookInstance using the decorator
    @admin.register(BookInstance)
    class BookInstanceAdmin(admin.ModelAdmin):
        pass

Currently all of our admin classes are empty (see pass) so the admin behavior will be unchanged! We can now extend these to define our model-specific admin behavior.

### Configure List View

The LocalLibrary currently lists all authors using the object name generated from the model __str__() method. This is fine when you only have a few authors, but once you have many you may end up having duplicates. To differentiate them, or just because you want to show more interesting information about each author, you can use list_display to add additional fields to the view. 

Replace your AuthorAdmin class with the code below. The field names to be displayed in the list are declared in a tuple in the required order, as shown (these are the same names as specified in your original model).

    class AuthorAdmin(admin.ModelAdmin):
        list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')

Now navigate to the author list in your website. The fields above should now be displayed, like so:

For our Book model we'll additionally display the author and genre. The author is a ForeignKey field (one-to-many) relationship, and so will be represented by the `__str__()` value for the associated record. Replace the BookAdmin class with the version below.

    class BookAdmin(admin.ModelAdmin):
        list_display = ('title', 'author', 'display_genre')

Unfortunately we can't directly specify the genre field in list_display because it is a ManyToManyField (Django prevents this because there would be a large database access "cost" in doing so). Instead we'll define a display_genre function to get the information as a string (this is the function we've called above; we'll define it below).

> **Note:** Getting the genre may not be a good idea here, because of the "cost" of the database operation. We're showing you how because calling functions in your models can be very useful for other reasons — for example to add a Delete link next to every item in the list.

Add the following code into your Book model (models.py). This creates a string from the first three values of the genre field (if they exist) and creates a short_description that can be used in the admin site for this method.

    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])

        display_genre.short_description = 'Genre'

After saving the model and updated admin, open your website and go to the Books list page; you should see a book list like the one below:

The Genre model (and the Language model, if you defined one) both have a single field, so there is no point creating an additional model for them to display additional fields.

> **Note:** It is worth updating the BookInstance model list to show at least the status and the expected return date. We've added that as a challenge at the end of this article!

### Add list filters

Once you've got a lot of items in a list, it can be useful to be able to filter which items are displayed. This is done by listing fields in the list_filter attribute. Replace your current BookInstanceAdmin class with the code fragment below.

    class BookInstanceAdmin(admin.ModelAdmin):
        list_filter = ('status', 'due_back')

The list view will now include a filter box to the right. Note how you can choose dates and status to filter the values:

### Organize detail view layout

By default, the detail views lay out all fields vertically, in their order of declaration in the model. You can change the order of declaration, which fields are displayed (or excluded), whether sections are used to organize the information, whether fields are displayed horizontally or vertically, and even what edit widgets are used in the admin forms.

> **Note:** The LocalLibrary models are relatively simple so there isn't a huge need for us to change the layout; we'll make some changes anyway however, just to show you how.

### Controlling which fields are displayed and laid out

Update your AuthorAdmin class to add the fields line, as shown below (in bold):

    class AuthorAdmin(admin.ModelAdmin):
        list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
        fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

The fields attribute lists just those fields that are to be displayed on the form, in order. Fields are displayed vertically by default, but will display horizontally if you further group them in a tuple (as shown in the "date" fields above).

In your website go to the author detail view — it should now appear as shown below:

> **Note:** You can also use the exclude attribute to declare a list of attributes to be excluded from the form (all other attributes in the model will be displayed).

### Sectioning the detail view

You can add "sections" to group related model information within the detail form, using the fieldsets attribute.

In the BookInstance model we have information related to what the book is (i.e. name, imprint, and id) and when it will be available (status, due_back). We can add these in different sections by adding the text in bold to our BookInstanceAdmin class. 

    @admin.register(BookInstance)
    class BookInstanceAdmin(admin.ModelAdmin):
        list_filter = ('status', 'due_back')

        fieldsets = (
            (None, {
                'fields': ('book', 'imprint', 'id')
            }),
            ('Availability', {
                'fields': ('status', 'due_back')
            }),
        )

Each section has its own title (or None, if you don't want a title) and an associated tuple of fields in a dictionary — the format is complicated to describe, but fairly easy to understand if you look at the code fragment immediately above.

Now navigate to a book instance view in your website; the form should appear as shown below:

### Inline editing of associated records

Sometimes it can make sense to be able to add associated records at the same time. For example, it may make sense to have both the book information and information about the specific copies you've got on the same detail page.

You can do this by declaring [inlines](https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.inlines), of type [TabularInline](https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#django.contrib.admin.TabularInline) (horizontal layout) or StackedInline (vertical layout, just like the default model layout). You can add the BookInstance information inline to our Book detail by adding the lines below in bold near your BookAdmin:

    class BooksInstanceInline(admin.TabularInline):
        model = BookInstance

    @admin.register(Book)
    class BookAdmin(admin.ModelAdmin):
        list_display = ('title', 'author', 'display_genre')
        inlines = [BooksInstanceInline]

Now navigate to a view for a Book in your website — at the bottom you should now see the book instances relating to this book (immediately below the book's genre fields):

In this case all we've done is declare our tabular inline class, which just adds all fields from the inlined model. You can specify all sorts of additional information for the layout, including the fields to display, their order, whether they are read only or not, etc. (see TabularInline for more information).

> **Note:** There are some painful limits in this functionality! In the screenshot above we have three existing book instances, followed by three placeholders for new book instances (which look very similar!). It would be better to have NO spare book instances by default and just add them with the Add another Book instance link, or to be able to just list the BookInstances as non-readable links from here. The first option can be done by setting the extra attribute to 0 in BooksInstanceInline model, try it by yourself.

### Challange

We've learned a lot in this section, so now it is time for you to try a few things.

- For the BookInstance list view, add code to display the book, status, due back date, and id (rather than the default `__str__()` text).
- Add an inline listing of Book items to the Author detail view using the same approach as we did for Book/BookInstance.

## Part 5: Creating Our Home Page

We're now ready to add the code that displays our first complete page — a home page for the LocalLibrary website. The home page will show the number of records we have for each model type and provide sidebar navigation links to our other pages. Along the way we'll gain practical experience in writing basic URL maps and views, getting records from the database, and using templates.

After we defined our models and created some initial library records to work with, it's time to write the code that presents that information to users. The first thing we need to do is determine what information we want to display in our pages, and define the URLs to use for returning those resources. Then we'll create a URL mapper, views, and templates to display the pages. 

The following diagram describes the main data flow, and the components required when handling HTTP requests and responses. As we already implemented the model, the main components we'll create are:

- URL mappers to forward the supported URLs (and any information encoded in the URLs) to the appropriate view functions.
- View functions to get the requested data from the models, create HTML pages that display the data, and return the pages to the user to view in the browser.
- Templates to use when rendering data in the views.

![Working of Views in Diagram](../../static/catalog/images/views.png)

As you'll see in the next section, we have 5 pages to display, which is too much information to document in a single article. Therefore, this article will focus on how to implement the home page, and we'll cover the other pages in a subsequent article. This should give you a good end-to-end understanding of how URL mappers, views, and models work in practice.

### Defining the resource URLs

As this version of LocalLibrary is essentially read-only for end users, we just need to provide a landing page for the site (a home page), and pages that display list and detail views for books and authors. 

The URLs that we'll need for our pages are:

- catalog/ — The home (index) page.
- catalog/books/ — A list of all books.
- catalog/authors/ — A list of all authors.
- catalog/book/`<id>` — The detail view for a particular book, with a field primary key of `<id>` (the default). For example, the URL for the third book added to the list will be /catalog/book/3.
- catalog/author/`<id>` — The detail view for the specific author with a primary key field of `<id>`. For example, the URL for the 11th author added to the list will be  /catalog/author/11.

The first three URLs will return the index page, books list, and authors list. These URLs do not encode any additional information, and the queries that fetch data from the database will always be the same. However, the results that the queries return will depend on the contents of the database.

By contrast the final two URLs will display detailed information about a specific book or author.  These URLs encode the identity of the item to display (represented by `<id>` above). The URL mapper will extract the encoded information and pass it to the view, and the view will dynamically determine what information to get from the database. By encoding the information in the URL we will use a single set of a url mapping, a view, and a template to handle all books (or authors).

> **Note:** With Django, you can construct your URLs however you require — you can encode information in the body of the URL as shown above, or include GET parameters in the URL, for example /book/?id=6. Whichever approach you use, the URLs should be kept clean, logical, and readable, as recommended by the W3C. The Django documentation recommends encoding information in the body of the URL to achieve better URL design.

### Creating the index page

The first page we'll create is the index page (catalog/). The index page will include some static HTML, along with generated "counts" of different records in the database. To make this work we'll create a URL mapping, a view, and a template. 

> **Note:** It's worth paying a little extra attention in this section. Most of the information also applies to the other pages we'll create.

### URL mapping

When we created the skeleton website, we updated the locallibrary/urls.py file to ensure that whenever a URL that starts with catalog/  is received, the URLConf module catalog.urls will process the remaining substring.

The following code snippet from locallibrary/urls.py includes the catalog.urls module:  

    urlpatterns += [
        path('catalog/', include('catalog.urls')),
    ]

> **Note:** Whenever Django encounters the import function django.urls.include(), it splits the URL string at the designated end character and sends the remaining substring to the included URLconf module for further processing.

We also created a placeholder file for the URLConf module, named /catalog/urls.py. Add the following lines to that file: 

    urlpatterns = [
        path('', views.index, name='index'),
    ]

The path() function defines the following:

- A URL pattern, which is an empty string: ''. We'll discuss URL patterns in detail when working on the other views.
- A view function that will be called if the URL pattern is detected: views.index,  which is the function named index() in the views.py file.

The path() function also specifies a name parameter, which is a unique identifier for this particular URL mapping. You can use the name to "reverse" the mapper, i.e.  to dynamically create a URL that  points to the resource that the mapper is designed to handle. For example, we can use the name parameter to link to our home page from any other page by adding the following link in a template:

    <a href="{% url 'index' %}">Home</a>

> **Note:** We can hard code the link as in `<a href="/catalog/">Home</a>)`, but if we change the pattern for our home page, for example, to /catalog/index) the templates will no longer link correctly. Using a reversed url mapping is more robust.

### View (function-based)

A view is a function that processes an HTTP request, fetches the required data from the database, renders the data in an HTML page using an HTML template, and then returns the generated HTML in an HTTP response to display the page to the user. The index view follows this model — it fetches information about the number of Book, BookInstance, available BookInstance and Author records that we have in the database, and passes that information to a template for display.

Open catalog/views.py and note that the file already imports the render() shortcut function to generate an HTML file using a template and data: 

    from django.shortcuts import render

    # Create your views here.

Paste the following lines at the bottom of the file:

    from catalog.models import Book, Author, BookInstance, Genre

    def index(request):
        """View function for home page of site."""

        # Generate counts of some of the main objects
        num_books = Book.objects.all().count()
        num_instances = BookInstance.objects.all().count()

        # Available books (status = 'a')
        num_instances_available = BookInstance.objects.filter(status__exact='a').count()

        # The 'all()' is implied by default.
        num_authors = Author.objects.count()

        context = {
            'num_books': num_books,
            'num_instances': num_instances,
            'num_instances_available': num_instances_available,
            'num_authors': num_authors,
        }

        # Render the HTML template index.html with the data in the context variable
        return render(request, 'index.html', context=context)

The first line imports the model classes that we'll use to access data in all our views.

The first part of the view function fetches the number of records using the objects.all() attribute on the model classes. It also gets a list of BookInstance objects that have a value of 'a' (Available) in the status field. You can find more information about how to access model data in our previous tutorial Django Tutorial Part 3: Using models > Searching for records.

At the end of the view function we call the render() function to create an HTML page and return the page as a response. This shortcut function wraps a number of other functions to simplify a very common use case. The render() function accepts the following parameters:

- the original request object, which is an HttpRequest.
- an HTML template with placeholders for the data.
- a context variable, which is a Python dictionary, containing the data to insert into the placeholders. 

We'll talk more about templates and the context variable in the next section.  Let's get to creating our template so we can actually display something to the user!

### Templates

A template is a text file that defines the structure or layout of a file (such as an HTML page), it uses placeholders to represent actual content. 

A Django application created using startapp (like the skeleton of this example) will look for templates in a subdirectory named 'templates' of your applications. For example, in the index view that we just added, the render() function will expect to find the file index.html in /locallibrary/catalog/templates/ and will raise an error if the file is not present.

You can check this by saving the previous changes and accessing 127.0.0.1:8000 in your browser - it will display a fairly intuitive error message: "TemplateDoesNotExist at /catalog/", and other details.

> **Note:** Based on your project's settings file, Django will look for templates in a number of places, searching in your installed applications by default. You can find out more about how Django finds templates and what template formats it supports in the Templates section of the Django documentation

### Extending templates

The index template will need standard HTML markup for the head and body, along with navigation sections to link to the other pages of the site (which we haven't created yet), and to sections that display introductory text and book data.

Much of the HTML and navigation structure will be the same in every page of our site. Instead of duplicating boilerplate code on every page, you can use the Django templating language to declare a base template, and then extend it to replace just the bits that are different for each specific page. 

The following code snippet is a sample base template from a base_generic.html file. We'll be creating the template for LocalLibrary shortly. The sample below includes common HTML with sections for a title, a sidebar, and main contents marked with the named block and endblock template tags, shown in bold. You can leave the blocks empty, or include default content to use when rendering pages derived from the template.

> **Note:** Template tags are functions that you can use in a template to loop through lists, perform conditional operations based on the value of a variable, and so on. In addition to template tags, the template syntax allows you to reference variables that are passed into the template from the view, and use template filters to format variables (for example, to convert a string to lower case).

    <!DOCTYPE html>
    <html lang="en">
    <head>
    {% block title %}<title>Local Library</title>{% endblock %}
    </head>
    <body>
    {% block sidebar %}<!-- insert default navigation text for every page -->{% endblock %}
    {% block content %}<!-- default content text (typically empty) -->{% endblock %}
    </body>
    </html>

When defining a template for a particular view, we first specify the base template using the extends template tag — see the code sample below. Then we declare what sections from the template we want to replace (if any), using block/endblock sections as in the base template. 

For example, the code snippet below shows how to use the extends template tag and override the content block. The generated HTML will include the code and structure defined in the base template, including the default content you defined in the title block, but the new content block in place of the default one.

    {% extends "base_generic.html" %}

    {% block content %}
    <h1>Local Library Home</h1>
    <p>Welcome to LocalLibrary, a website developed by <em>Mozilla Developer Network</em>!</p>
    {% endblock %}

### The LocalLibrary Base Template

We will use the following code snippet as the base template for the LocalLibrary website. As you can see, it contains some HTML code and defines blocks for title, sidebar, and content. We have a default title and a default sidebar with links to lists of all books and authors, both enclosed in blocks to be easily changed in the future.

> **Note:** We also introduce two additional template tags: url and load static. These tags will be explained in following sections.

Create a new file **base_generic.html** in **/locallibrary/catalog/templates/** and paste the following code to the file:

    <!DOCTYPE html>
    <html lang="en">
    <head>
    {% block title %}<title>Local Library</title>{% endblock %}
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css" integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">
    <!-- Add additional CSS in static file -->
    {% load static %}
    <link rel="stylesheet" href="{% static 'css/styles.css' %}">
    </head>
    <body>
    <div class="container-fluid">
        <div class="row">
        <div class="col-sm-2">
        {% block sidebar %}
            <ul class="sidebar-nav">
            <li><a href="{% url 'index' %}">Home</a></li>
            <li><a href="">All books</a></li>
            <li><a href="">All authors</a></li>
            </ul>
        {% endblock %}
        </div>
        <div class="col-sm-10 ">{% block content %}{% endblock %}</div>
        </div>
    </div>
    </body>
    </html>

The template includes CSS from Bootstrap to improve the layout and presentation of the HTML page. Using Bootstrap (or another client-side web framework) is a quick way to create an attractive page that displays well on different screen sizes.

The base template also references a local css file (styles.css) that provides additional styling. Create a styles.css file in **/locallibrary/catalog/static/css/** and paste the following code in the file:

    .sidebar-nav {
        margin-top: 20px;
        padding: 0;
        list-style: none;
    }

### The index template

Create a new HTML file index.html in /locallibrary/catalog/templates/ and paste the following code in the file. This code extends our base template on the first line, and then replaces the default content block for the template. 

    {% extends "base_generic.html" %}

    {% block content %}
    <h1>Local Library Home</h1>
    <p>Welcome to LocalLibrary, a website developed by <em>Mozilla Developer Network</em>!</p>
    <h2>Dynamic content</h2>
    <p>The library has the following record counts:</p>
    <ul>
        <li><strong>Books:</strong> {{ num_books }}</li>
        <li><strong>Copies:</strong> {{ num_instances }}</li>
        <li><strong>Copies available:</strong> {{ num_instances_available }}</li>
        <li><strong>Authors:</strong> {{ num_authors }}</li>
    </ul>
    {% endblock %}

In the Dynamic content section we declare placeholders (template variables) for the information from the view that we want to include. The variables are enclosed with double brace (handlebars), as shown in bold in the code sample. 

> **Note:** You can easily recognize template variables and template tags (functions) - variables are enclosed in double braces ({{ num_books }}), and tags are enclosed in single braces with percentage signs ({% extends "base_generic.html" %}).

The important thing to note here is that variables are named with the keys that we pass into the context dictionary in the render() function of our view (see sample below). Variables will be replaced with their associated values when the template is rendered.

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    return render(request, 'index.html', context=context)

### Referencing static files in templates

Your project is likely to use static resources, including JavaScript, CSS, and images. Because the location of these files might not be known (or might change), Django allows you to specify the location in your templates relative to the STATIC_URL global setting. The default skeleton website sets the value of STATIC_URL to '/static/', but you might choose to host these on a content delivery network or elsewhere.

Within the template you first call the load template tag specifying "static" to add the template library, as shown in the code sample below. You can then use the static template tag and specify the relative URL to the required file.

    <!-- Add additional CSS in static file -->
    {% load static %}
    <link rel="stylesheet" href="{% static 'css/styles.css' %}">

You can add an image into the page in a similar way, for example:

    {% load static %}
    <img src="{% static 'catalog/images/local_library_model_uml.png' %}" alt="UML diagram" style="width:555px;height:540px;">

> **Note:** The samples above specify where the files are located, but Django does not serve them by default. We configured the development web server to serve files by modifying the global URL mapper (/locallibrary/locallibrary/urls.py) when we created the website skeleton, but still need to enable file serving in production. We'll look at this later.

For more information on working with static files see [Managing static files](https://docs.djangoproject.com/en/3.1/howto/static-files/) in the Django documentation.

### Linking to URLS

The base template above introduced the url template tag

    <li><a href="{% url 'index' %}">Home</a></li>

This tag accepts the name of a path() function called in your urls.py and the values for any arguments that the associated view will receive from that function, and returns a URL that you can use to link to the resource.

### Configuring where to find Templates

The location where Django searches for templates is specified in the TEMPLATES object in the settings.py file. The default settings.py (as created for this tutorial) looks something like this:

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

The setting of 'APP_DIRS': True, is the most important, as it tells Django to search for templates in a subdirectory of each application in the project, named "templates" (this makes it easier to group templates with their associated application for easy re-use).

We can also specify specific locations for Django to search for directories using 'DIRS': [] (but that isn't needed yet).

> **Note:** You can find out more about how Django finds templates and what template formats it supports in the [Templates section of the Django documentation](https://docs.djangoproject.com/en/3.1/topics/templates/)
> The All books and All authors links will not work yet because the paths, views, and templates for those pages are not defined. We just inserted placeholders for those links in the base_generic.html template.

## Part 6: Generic list and detail views

This tutorial extends our LocalLibrary website, adding list and detail pages for books and authors. Here we'll learn about generic class-based views, and show how they can reduce the amount of code you have to write for common use cases. We'll also go into URL handling in greater detail, showing how to perform basic pattern matching.

In this tutorial we're going to complete the first version of the LocalLibrary website by adding list and detail pages for books and authors (or to be more precise, we'll show you how to implement the book pages, and get you to create the author pages yourself!)

The process is similar to creating the index page, which we showed in the previous tutorial. We'll still need to create URL maps, views, and templates. The main difference is that for the detail pages, we'll have the additional challenge of extracting information from patterns in the URL and passing it to the view. For these pages, we're going to demonstrate a completely different type of view: generic class-based list and detail views. These can significantly reduce the amount of view code needed, making them easier to write and maintain.

The final part of the tutorial will demonstrate how to paginate your data when using generic class-based list views.

### Book List Page

The book list page will display a list of all the available book records in the page, accessed using the URL: catalog/books/. The page will display a title and author for each record, with the title being a hyperlink to the associated book detail page. The page will have the same structure and navigation as all other pages in the site, and we can, therefore, extend the base template (base_generic.html) we created in the previous tutorial.

### URL mapping

Open /catalog/urls.py and copy in the line shown in bold below. As for the index page, this path() function defines a pattern to match against the URL ('books/'), a view function that will be called if the URL matches (views.BookListView.as_view()), and a name for this particular mapping.

    urlpatterns = [
        path('', views.index, name='index'),
        path('books/', views.BookListView.as_view(), name='books'),
    ]

As discussed in the previous tutorial the URL must already have matched /catalog, so the view will actually be called for the URL: /catalog/books/.

The view function has a different format than before — that's because this view will actually be implemented as a class. We will be inheriting from an existing generic view function that already does most of what we want this view function to do, rather than writing our own from scratch.

For Django class-based views we access an appropriate view function by calling the class method as_view(). This does all the work of creating an instance of the class, and making sure that the right handler methods are called for incoming HTTP requests.

### View (class based)

We could quite easily write the book list view as a regular function (just like our previous index view), which would query the database for all books, and then call render() to pass the list to a specified template. Instead, however, we're going to use a class-based generic list view (ListView) — a class that inherits from an existing view. Because the generic view already implements most of the functionality we need and follows Django best-practice, we will be able to create a more robust list view with less code, less repetition, and ultimately less maintenance.

Open **catalog/views.py**, and copy the following code into the bottom of the file:

    from django.views import generic

    class BookListView(generic.ListView):
        model = Book

That's it! The generic view will query the database to get all records for the specified model (Book) then render a template located at **/locallibrary/catalog/templates/catalog/book_list.html** (which we will create below). Within the template you can access the list of books with the template variable named object_list OR book_list (i.e. generically "the_model_name_list").

> **Note:** This awkward path for the template location isn't a misprint — the generic views look for templates in /application_name/the_model_name_list.html (catalog/book_list.html in this case) inside the application's /application_name/templates/ directory (/catalog/templates/)

You can add attributes to change the default behavior above. For example, you can specify another template file if you need to have multiple views that use this same model, or you might want to use a different template variable name if book_list is not intuitive for your particular template use-case. Possibly the most useful variation is to change/filter the subset of results that are returned — so instead of listing all books you might list top 5 books that were read by other users.

    class BookListView(generic.ListView):
        model = Book
        context_object_name = 'my_book_list'   # your own name for the list as a template variable
        queryset = Book.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title war
        template_name = 'books/my_arbitrary_template_name_list.html'  # Specify your own template name/location

### Overriding methods in class-based views

While we don't need to do so here, you can also override some of the class methods.

For example, we can override the get_queryset() method to change the list of records returned. This is more flexible than just setting the queryset attribute as we did in the preceding code fragment (though there is no real benefit in this case):

    class BookListView(generic.ListView):
        model = Book

        def get_queryset(self):
            return Book.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title war

We might also override get_context_data() in order to pass additional context variables to the template (e.g. the list of books is passed by default). The fragment below shows how to add a variable named "some_data" to the context (it would then be available as a template variable).

    class BookListView(generic.ListView):
        model = Book

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(BookListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context

When doing this it is important to follow the pattern used above:

- First get the existing context from our superclass.
- Then add your new context information. 
- Then return the new (updated) context.

> **Note:** Check out Built-in [class-based generic views](https://docs.djangoproject.com/en/3.1/topics/class-based-views/generic-display/) (Django docs) for many more examples of what you can do.

### Creating the list view template

Create the HTML file /locallibrary/catalog/templates/catalog/book_list.html and copy in the text below. As discussed above, this is the default template file expected by the generic class-based list view (for a model named Book in an application named catalog).

Templates for generic views are just like any other templates (although of course the context/information passed to the template may differ). As with our index template, we extend our base template in the first line and then replace the block named content.

    {% extends "base_generic.html" %}

    {% block content %}
    <h1>Book List</h1>
    {% if book_list %}
    <ul>
        {% for book in book_list %}
        <li>
            <a href="{{ book.get_absolute_url }}">{{ book.title }}</a> ({{book.author}})
        </li>
        {% endfor %}
    </ul>
    {% else %}
        <p>There are no books in the library.</p>
    {% endif %} 
    {% endblock %}

The view passes the context (list of books) by default as object_list and book_list aliases; either will work.

### Conditional execution

We use the if, else, and endif template tags to check whether the book_list has been defined and is not empty. If book_list is empty, then the else clause displays text explaining that there are no books to list. If book_list is not empty, then we iterate through the list of books.

    {% if book_list %}
    <!-- code here to list the books -->
    {% else %}
    <p>There are no books in the library.</p>
    {% endif %}

The condition above only checks for one case, but you can test on additional conditions using the elif template tag (e.g. {% elif var2 %}). For more information about conditional operators see: if, [ifequal/ifnotequal](https://docs.djangoproject.com/en/3.1/ref/templates/builtins/#ifequal-and-ifnotequal), and [ifchanged](https://docs.djangoproject.com/en/3.1/ref/templates/builtins/#ifchanged) in [Built-in template tags](https://docs.djangoproject.com/en/3.1/ref/templates/builtins/) and filters (Django Docs).

### For Loops

The template uses the [for](https://docs.djangoproject.com/en/3.1/ref/templates/builtins/#for) and endfor template tags to loop through the book list, as shown below. Each iteration populates the book template variable with information for the current list item.

    {% for book in book_list %}
    <li> <!-- code here get information from each book item --> </li>
    {% endfor %}

While not used here, within the loop Django will also create other variables that you can use to track the iteration. For example, you can test the forloop.last variable to perform conditional processing the last time that the loop is run.

### Accessing variables

The code inside the loop creates a list item for each book that shows both the title (as a link to the yet-to-be-created detail view) and the author.

    <a href="{{ book.get_absolute_url }}">{{ book.title }}</a> ({{book.author}})

We access the fields of the associated book record using the "dot notation" (e.g. book.title and book.author), where the text following the book item is the field name (as defined in the model).

We can also call functions in the model from within our template — in this case we call Book.get_absolute_url() to get a URL you could use to display the associated detail record. This works provided the function does not have any arguments (there is no way to pass arguments!)

**NOTE:** We have to be a little careful of "side effects" when calling functions in templates. Here we just get a URL to display, but a function can do pretty much anything — we wouldn't want to delete our database (for example) just by rendering our template!

### Update the base template

Open the base template (/locallibrary/catalog/templates/base_generic.html) and insert {% url 'books' %} into the URL link for All books, as shown below. This will enable the link in all pages (we can successfully put this in place now that we've created the "books" URL mapper).

    <li><a href="{% url 'index' %}">Home</a></li>
    <li><a href="{% url 'books' %}">All books</a></li>
    <li><a href="">All authors</a></li>

### What does it look like?

You won't be able to build the book list yet, because we're still missing a dependency — the URL map for the book detail pages, which is needed to create hyperlinks to individual books. We'll show both list and detail views after the next section.

### Book Detail Page

The book detail page will display information about a specific book, accessed using the URL **`catalog/book/<id>`** (where `<id>` is the primary key for the book). In addition to fields in the Book model (author, summary, ISBN, language, and genre), we'll also list the details of the available copies (BookInstances) including the status, expected return date, imprint, and id. This will allow our readers to not only learn about the book, but also to confirm whether/when it is available.

### URL mapping

Open /catalog/urls.py and add the 'book-detail' URL mapper shown in bold below. This path() function defines a pattern, associated generic class-based detail view, and a name.

    urlpatterns = [
        path('', views.index, name='index'),
        path('books/', views.BookListView.as_view(), name='books'),
        path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    ]

For the book-detail path the URL pattern uses a special syntax to capture the specific id of the book that we want to see. The syntax is very simple: angle brackets define the part of the URL to be captured, enclosing the name of the variable that the view can use to access the captured data. For example, `<something>` , will capture the marked pattern and pass the value to the view as a variable "something". You can optionally precede the variable name with a [converter specification](https://docs.djangoproject.com/en/3.1/topics/http/urls/#path-converters) that defines the type of data (int, str, slug, uuid, path).

In this case we use `'<int:pk>'` to capture the book id, which must be a specially formatted string and pass it to the view as a parameter named pk (short for primary key). This is the id that is being used to store the book uniquely in the database, as defined in the Book Model.

> **NOTE:** As discussed previously, our matched URL is actually catalog/book/`<digits>` (because we are in the catalog application, /catalog/ is assumed).

> ***IMPORTANT:*** The generic class-based detail view expects to be passed a parameter named pk. If you're writing your own function view you can use whatever parameter name you like, or indeed pass the information in an unnamed argument.

### Advanced path matching/regular expression primer

> **NOTE:** You won't need this section to complete the tutorial! We provide it because knowing this option is likely to be useful in your Django-centric future.

The pattern matching provided by path() is simple and useful for the (very common) cases where you just want to capture any string or integer. If you need more refined filtering (for example, to filter only strings that have a certain number of characters) then you can use the [re_path()](https://docs.djangoproject.com/en/3.1/ref/urls/#django.urls.re_path) method.

This method is used just like path() except that it allows you to specify a pattern using a [Regular expression](https://docs.python.org/3/library/re.html). For example, the previous path could have been written as shown below:

    re_path(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book-detail'),

Regular expressions are an incredibly powerful pattern mapping tool. They are, frankly, quite unintuitive and can be intimidating for beginners. Below is a very short primer!

The first thing to know is that regular expressions should usually be declared using the raw string literal syntax (i.e. they are enclosed as shown: `r'<your regular expression text goes here>').`

The main parts of the syntax you will need to know for declaring the pattern matches are:

    Symbol	    Meaning
    -------------------------------------------------------
    ^	        Match the beginning of the text

    $	        Match the end of the text
    
    \d	        Match a digit (0, 1, 2, ... 9)
    
    \w	        Match a word character, e.g. any upper- or lower-case character in the alphabet, digit or the underscore character (_)
    
    +	        Match one or more of the preceding character. For example, to match one or more digits you would use \d+. To match one or more "a" characters, you could use a+
    
    *	        Match zero or more of the preceding character. For example, to match nothing or a word you could use \w*

    ( )	        Capture the part of the pattern inside the brackets. Any captured values will be passed to the view as unnamed parameters (if multiple patterns are captured, the associated parameters will be supplied in the order that the captures were declared).

    (?P<name>...)	Capture the pattern (indicated by ...) as a named variable (in this case "name"). The captured values are passed to the view with the name specified. Your view must therefore declare a parameter with the same name!
    
    [  ]	        Match against one character in the set. For example, [abc] will match on 'a' or 'b' or 'c'. [-\w] will match on the '-' character or any word character.

Most other characters can be taken literally!

Let's consider a few real examples of patterns:

    Pattern	                    Description
    r'^book/(?P<pk>\d+)$'	    This is the RE used in our URL mapper. It matches a string that has book/ at the start of the line (^book/), then has one or more digits (\d+), and then ends (with no non-digit characters before the end of line marker).

                                It also captures all the digits (?P<pk>\d+) and passes them to the view in a parameter named 'pk'. The captured values are always passed as a string!

                                For example, this would match book/1234 , and send a variable pk='1234' to the view.

    r'^book/(\d+)$'	             This matches the same URLs as the preceding case. The captured information would be sent as an unnamed argument to the view.
    
    r'^book/(?P<stub>[-\w]+)$'	This matches a string that has book/ at the start of the line (^book/), then has one or more characters that are either a '-' or a word character ([-\w]+), and then ends. It also captures this set of characters and passes them to the view in a parameter named 'stub'.

                                This is a fairly typical pattern for a "stub". Stubs are URL-friendly word-based primary keys for data. You might use a stub if you wanted your book URL to be more informative. For example /catalog/book/the-secret-garden rather than /catalog/book/33.

You can capture multiple patterns in the one match, and hence encode lots of different information in a URL.

> **NOTE:** As a challenge, consider how you might encode a URL to list all books released in a particular year, month, day, and the RE that could be used to match it.

### Passing additional options in your URL maps

One feature that we haven't used here, but which you may find valuable, is that you can pass a [dictionary containing additional options](https://docs.djangoproject.com/en/3.1/topics/http/urls/#views-extra-options) to the view (using the third un-named argument to the path() function). This approach can be useful if you want to use the same view for multiple resources, and pass data to configure its behavior in each case.

For example, given the path shown below, for a request to /myurl/halibut/ Django will call views.my_view(request, fish=halibut, my_template_name='some_path').

    path('myurl/<int:fish>', views.my_view, {'my_template_name': 'some_path'}, name='aurl'),

> **NOTE:** Both named captured patterns and dictionary options are passed to the view as named arguments. If you use the same name for both a capture pattern and a dictionary key, then the dictionary option will be used.

### View Class Based

Open catalog/views.py, and copy the following code into the bottom of the file:

    class BookDetailView(generic.DetailView):
    model = Book

That's it! All you need to do now is create a template called /locallibrary/catalog/templates/catalog/book_detail.html, and the view will pass it the database information for the specific Book record extracted by the URL mapper. Within the template you can access the book's details with the template variable named object OR book (i.e. generically "the_model_name").

If you need to, you can change the template used and the name of the context object used to reference the book in the template. You can also override methods to, for example, add additional information to the context.

### What if record doesn't exist?

If a requested record does not exist then the generic class-based detail view will raise an Http404 exception for you automatically — in production, this will automatically display an appropriate "resource not found" page, which you can customise if desired.

Just to give you some idea of how this works, the code fragment below demonstrates how you would implement the class-based view as a function if you were not using the generic class-based detail view.

    def book_detail_view(request, primary_key):
    try:
        book = Book.objects.get(pk=primary_key)
    except Book.DoesNotExist:
        raise Http404('Book does not exist')

    return render(request, 'catalog/book_detail.html', context={'book': book})

The view first tries to get the specific book record from the model. If this fails the view should raise an Http404 exception to indicate that the book is "not found". The final step is then, as usual, to call render() with the template name and the book data in the context parameter (as a dictionary).

Alternatively, we can use the get_object_or_404() function as a shortcut to raise an Http404 exception if the record is not found.

    from django.shortcuts import get_object_or_404

    def book_detail_view(request, primary_key):
        book = get_object_or_404(Book, pk=primary_key)
        return render(request, 'catalog/book_detail.html', context={'book': book})

### Creating the Detail View Template

Create the HTML file /locallibrary/catalog/templates/catalog/book_detail.html and give it the below content. As discussed above, this is the default template file name expected by the generic class-based detail view (for a model named Book in an application named catalog).

    {% extends "base_generic.html" %}

    {% block content %}
    <h1>Title: {{ book.title }}</h1>

    <p><strong>Author:</strong> <a href="">{{ book.author }}</a></p> <!-- author detail link not yet defined -->
    <p><strong>Summary:</strong> {{ book.summary }}</p>
    <p><strong>ISBN:</strong> {{ book.isbn }}</p>
    <p><strong>Language:</strong> {{ book.language }}</p>
    <p><strong>Genre:</strong> {{ book.genre.all|join:", " }}</p>

    <div style="margin-left:20px;margin-top:20px">
        <h4>Copies</h4>

        {% for copy in book.bookinstance_set.all %}
        <hr>
        <p class="{% if copy.status == 'a' %}text-success{% elif copy.status == 'm' %}text-danger{% else %}text-warning{% endif %}">
            {{ copy.get_status_display }}
        </p>
        {% if copy.status != 'a' %}
            <p><strong>Due to be returned:</strong> {{ copy.due_back }}</p>
        {% endif %}
        <p><strong>Imprint:</strong> {{ copy.imprint }}</p>
        <p class="text-muted"><strong>Id:</strong> {{ copy.id }}</p>
        {% endfor %}
    </div>
    {% endblock %}

***
**NOTE:** The author link in the template above has an empty URL because we've not yet created an author detail page to link to. Once the detail page exists we can get its URL with either of these two approaches:

 - Use the url template tag to reverse the 'author-detail' URL (defined in the URL mapper), passing it the author instance for the book:

        <a href="{% url 'author-detail' book.author.pk %}">{{ book.author }}</a>

- Call the author model's get_absolute_url() method (this performs the same reversing operation):

        <a href="{{ book.author.get_absolute_url }}">{{ book.author }}</a>

While both methods effectively do the same thing, get_absolute_url() is preferred because it helps you write more consistent and maintainable code (any changes only need to be done in one place: the author model).

Though a little larger, almost everything in this template has been described previously:

- We extend our base template and override the "content" block.
- We use conditional processing to determine whether or not to display specific content.
- We use for loops to loop through lists of objects.
- We access the context fields using the dot notation (because we've used the detail generic view, the context is named book; we could also use "object")

The first interesting thing we haven't seen before is the function book.bookinstance_set.all(). This method is "automagically" constructed by Django in order to return the set of BookInstance records associated with a particular Book.

    {% for copy in book.bookinstance_set.all %}
    <!-- code to iterate across each copy/instance of a book -->
    {% endfor %}

This method is needed because you declare a ForeignKey (one-to many) field in only the "one" side of the relationship (the BookInstance). Since you don't do anything to declare the relationship in the other ("many") models, it (the Book) doesn't have any field to get the set of associated records. To overcome this problem, Django constructs an appropriately named "reverse lookup" function that you can use. The name of the function is constructed by lower-casing the model name where the ForeignKey was declared, followed by _set (i.e. so the function created in Book is bookinstance_set()).

**NOTE:**
Here we use all() to get all records (the default). While you can use the filter() method to get a subset of records in code, you can't do this directly in templates because you can't specify arguments to functions.

Beware also that if you don't define an order (on your class-based view or model), you will also see errors from the development server like this one:

    [29/May/2017 18:37:53] "GET /catalog/books/?page=1 HTTP/1.1" 200 1637
    /foo/local_library/venv/lib/python3.5/site-packages/django/views/generic/list.py:99: UnorderedObjectListWarning: Pagination may yield inconsistent results with an unordered object_list: <QuerySet [<Author: Ortiz, David>, <Author: H. McRaven, William>, <Author: Leigh, Melinda>]>
    allow_empty_first_page=allow_empty_first_page, **kwargs)

That happens because the paginator object expects to see some ORDER BY being executed on your underlying database. Without it, it can't be sure the records being returned are actually in the right order!

This tutorial hasn't covered Pagination (yet!), but since you can't use sort_by() and pass a parameter (the same with filter() described above) you will have to choose between three choices:

1. Add a ordering inside a class Meta declaration on your model.
2. Add a queryset attribute in your custom class-based view, specifying an order_by().
3. Adding a get_queryset method to your custom class-based view and also specify the order_by().

If you decide to go with a class Meta for the Author model (probably not as flexible as customizing the class-based view, but easy enough), you will end up with something like this:

    class Author(models.Model):
        first_name = models.CharField(max_length=100)
        last_name = models.CharField(max_length=100)
        date_of_birth = models.DateField(null=True, blank=True)
        date_of_death = models.DateField('Died', null=True, blank=True)

        def get_absolute_url(self):
            return reverse('author-detail', args=[str(self.id)])

        def __str__(self):
            return f'{self.last_name}, {self.first_name}'

        class Meta:
            ordering = ['last_name']

Of course, the field doesn't need to be last_name: it could be any other.

Last but not least, you should sort by an attribute/column that actually has an index (unique or not) on your database to avoid performance issues. Of course, this will not be necessary here (we are probably getting ahead of ourselves with so few books and users), but it is something worth keeping in mind for future projects.

The second interesting (and non-obvious) thing in the template is where we set a class (text-success, text-danger, text-warning) to color-code the human readable status text for each book instance ("available", "maintenance", etc.). Astute readers will note that the method BookInstance.get_status_display() that we use to get the status text does not appear elsewhere in the code.

    <p class="{% if copy.status == 'a' %}text-success{% elif copy.status == 'm' %}text-danger{% else %}text-warning{% endif %}">
    {{ copy.get_status_display }} </p>

This function is automatically created because BookInstance.status is a choices field. Django automatically creates a method get_FOO_display() for every choices field "Foo" in a model, which can be used to get the current value of the field.

### What does it look like?

At this point, we should have created everything needed to display both the book list and book detail pages. Run the server (python3 manage.py runserver) and open your browser to http://127.0.0.1:8000/.

> *Warning:* Don't click any author or author detail links yet — you'll create those in the challenge!

Click the All books link to display the list of books.

### Pagination

If you've just got a few records, our book list page will look fine. However, as you get into the tens or hundreds of records the page will take progressively longer to load (and have far too much content to browse sensibly). The solution to this problem is to add pagination to your list views, reducing the number of items displayed on each page. 

Django has excellent inbuilt support for pagination. Even better, this is built into the generic class-based list views so you don't have to do very much to enable it!

**Views**
Open catalog/views.py, and add the paginate_by line shown in bold below.

    class BookListView(generic.ListView):
        model = Book
        paginate_by = 10

With this addition, as soon as you have more than 10 records the view will start paginating the data it sends to the template. The different pages are accessed using GET parameters — to access page 2 you would use the URL /catalog/books/?page=2

### Templates

Now that the data is paginated, we need to add support to the template to scroll through the results set. Because we might want paginate all list views, we'll add this to the base template. 

Open /locallibrary/catalog/templates/base_generic.html and find the "content block" (as shown below).

    {% block content %}{% endblock %}

Copy in the following pagination block immediately following the {% endblock %}. The code first checks if pagination is enabled on the current page. If so, it adds next and previous links as appropriate (and the current page number).

    {% block pagination %}
        {% if is_paginated %}
            <div class="pagination">
                <span class="page-links">
                    {% if page_obj.has_previous %}
                        <a href="{{ request.path }}?page={{ page_obj.previous_page_number }}">previous</a>
                    {% endif %}
                    <span class="page-current">
                        Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}.
                    </span>
                    {% if page_obj.has_next %}
                        <a href="{{ request.path }}?page={{ page_obj.next_page_number }}">next</a>
                    {% endif %}
                </span>
            </div>
        {% endif %}
    {% endblock %}

The page_obj is a Paginator object that will exist if pagination is being used on the current page. It allows you to get all the information about the current page, previous pages, how many pages there are, etc. 

We use {{ request.path }} to get the current page URL for creating the pagination links. This is useful because it is independent of the object that we're paginating.

That's it!

### What does it look like?

The screenshot below shows what the pagination looks like — if you haven't entered more than 10 titles into your database, then you can test it more easily by lowering the number specified in the paginate_by line in your catalog/views.py file. To get the below result we changed it to paginate_by = 2.

The pagination links are displayed on the bottom, with next/previous links being displayed depending on which page you're on.
