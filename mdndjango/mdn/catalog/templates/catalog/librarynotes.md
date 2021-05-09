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

