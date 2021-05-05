# Learning Django

## Initial Setup of Venv

- Pip freeze - in command line type pip freeze, it will show if virtual env, required or not.
- If Virtual env is available. Then type command as below
  
  ***python3 -m venv venv***.
  
  I have used venv twice. Second time it is used to mention directory, I prefer to choose the same dir.
- ***Activate Venv*** type in CMD.. source/venv/bin/activate
- To end Venv env.. type exit
- Now you have install what ever lib you need to get start with, like pip install django, pip install markdown etc...

## Start Django Project

### Creating Project with Django

If this is your first time using Django, you’ll have to take care of some initial setup. Namely, you’ll need to auto-generate some code that establishes a Django project – a collection of settings for an instance of Django, including database configuration, Django-specific options and application-specific settings.

From the command line, cd into a directory where you’d like to store your code, then run the following command:
`$ django-admin startproject (name of project)` I am going to use name mysite.
This will create a mysite directory in your current directory. If it didn’t work, see [Problems running django-admin](https://docs.djangoproject.com/en/3.2/faq/troubleshooting/#troubleshooting-django-admin)

> **Note:** You’ll need to avoid naming projects after built-in Python or Django components. In particular, this means you should avoid using names like django (which will conflict with Django itself) or test (which conflicts with a built-in Python package).
> **Where should this code live?**
    If your background is in plain old PHP (with no use of modern frameworks), you’re probably used to putting code under the Web server’s document root (in a place such as /var/www). With Django, you don’t do that. It’s not a good idea to put any of this Python code within your Web server’s document root, because it risks the possibility that people may be able to view your code over the Web. That’s not good for security.
    Put your code in some directory outside of the document root, such as /home/mycode.

Let’s look at what startproject created:

    mysite/
        manage.py
        mysite/
            __init__.py
            settings.py
            urls.py
            asgi.py
            wsgi.py

These files are:

- The outer **mysite/ root directory** is a container for your project. Its name doesn’t matter to Django; you can rename it to anything you like.
- **manage.py:** A command-line utility that lets you interact with this Django project in various ways. You can read all the details about manage.py in [django-admin and manage.py](https://docs.djangoproject.com/en/3.2/ref/django-admin/)
- The inner **mysite/ directory** is the actual Python package for your project. Its name is the Python package name you’ll need to use to import anything inside it (e.g. mysite.urls).
- **mysite/__init__.py:** An empty file that tells Python that this directory should be considered a Python package. If you’re a Python beginner, read [more about packages](https://docs.python.org/3/tutorial/modules.html#tut-packages) in the official Python docs.
- **mysite/settings.py:** Settings/configuration for this Django project. [Django settings](https://docs.djangoproject.com/en/3.2/topics/settings/) will tell you all about how settings work.
- **mysite/urls.py:** The URL declarations for this Django project; a “table of contents” of your Django-powered site. You can read more about URLs in [URL dispatcher.](https://docs.djangoproject.com/en/3.2/topics/http/urls/)
- **mysite/asgi.py:** An entry-point for ASGI-compatible web servers to serve your project. See [How to deploy with ASGI](https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/) for more details.
- **mysite/wsgi.py:** An entry-point for WSGI-compatible web servers to serve your project. See [How to deploy with WSGI](https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/) for more details.

## The development server

Let’s verify your Django project works. Change into the outer mysite directory, if you haven’t already, and run the following commands:
**`python3 manage.py runserver`**

You’ll see the following output on the command line:

    Performing system checks...
    System check identified no issues (0 silenced).

    You have unapplied migrations; your app may not work properly until they are applied.
    Run 'python manage.py migrate' to apply them.

    May 04, 2021 - 15:50:53
    Django version 3.2, using settings 'mysite.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.

You’ve started the Django development server, a lightweight Web server written purely in Python. We’ve included this with Django so you can develop things rapidly, without having to deal with configuring a production server – such as Apache – until you’re ready for production.

Now’s a good time to note: don’t use this server in anything resembling a production environment. It’s intended only for use while developing. (We’re in the business of making Web frameworks, not Web servers.)

Now that the server’s running, visit <http://127.0.0.1:8000/> with your Web browser. You’ll see a “Congratulations!” page, with a rocket taking off. It worked!

## Creating the app

Now that your environment – a “project” – is set up, you’re set to start doing work.

Each application you write in Django consists of a Python package that follows a certain convention. Django comes with a utility that automatically generates the basic directory structure of an app, so you can focus on writing code rather than creating directories.

> **Project vs Apps** : What’s the difference between a project and an app? An app is a Web application that does something – e.g., a Weblog system, a database of public records or a small poll app. A project is a collection of configuration and apps for a particular website. A project can contain multiple apps. An app can be in multiple projects.

Your apps can live anywhere on your Python path. In this tutorial, we’ll create our poll app in the same directory as your manage.py file so that it can be imported as its own top-level module, rather than a submodule of mysite.

To create your app, make sure you’re in the same directory as manage.py and type this command:

**`python3 manage.py startapp (app name) i'm using polls`**

That’ll create a directory polls, which is laid out like this:

    polls/
        __init__.py
        admin.py
        apps.py
        migrations/
            __init__.py
        models.py
        tests.py
        views.py

This directory structure will house the poll application

## Write your First View

Let’s write the first view. Open the file polls/views.py and put the following Python code in it:

    polls/views.py
    from django.http import HttpResponse

    def index(request):
        return HttpResponse("Hello World")

This is the simplest view possible in Django. To call the view, we need to map it to a URL - and for this we need a URLconf.

To create a URLconf in the polls directory, create a file called urls.py. Your app directory should now look like:

        polls/
            __init__.py
            admin.py
            apps.py
            migrations/
                __init__.py
            models.py
            tests.py
            urls.py
            views.py

In the polls/urls.py file include the following code

        polls/urls.py
        from django.urls import path

        from polls import views
        urlpatterns = [
            path("", views.index, name="index")
        ]

The next step is to point the root URLconf at the polls.urls module. In mysite/urls.py, add an import for django.urls.include and insert an include() in the urlpatterns list, so you have:

        mysite/urls.py
        from django.contrib import admin
        from django.urls import include, path

        urlpatterns = [
            path('polls/', include('polls.urls')),
            path('admin/', admin.site.urls),
        ]
The include() function allows referencing other URLconfs. Whenever Django encounters include(), it chops off whatever part of the URL matched up to that point and sends the remaining string to the included URLconf for further processing.

The idea behind include() is to make it easy to plug-and-play URLs. Since polls are in their own URLconf (polls/urls.py), they can be placed under “/polls/”, or under “/fun_polls/”, or under “/content/polls/”, or any other path root, and the app will still work.

> **When to use include()**
    You should always use include() when you include other URL patterns. admin.site.urls is the only exception to this.

You have now wired an index view into the URLconf. Verify it’s working with the following command:

**`python manage.py runserver`**

if you find page not found error check below

> **Page not found?** If you get an error page here, check that you’re going to <http://localhost:8000/polls/> and not <http://localhost:8000/>.

The path() function is passed four arguments, two required: route and view, and two optional: kwargs, and name. At this point, it’s worth reviewing what these arguments are for.

**path() argument: route**
route is a string that contains a URL pattern. When processing a request, Django starts at the first pattern in urlpatterns and makes its way down the list, comparing the requested URL against each pattern until it finds one that matches.

Patterns don’t search GET and POST parameters, or the domain name. For example, in a request to <https://www.example.com/myapp/>, the URLconf will look for myapp/. In a request to <https://www.example.com/myapp/?page=3>, the URLconf will also look for myapp/.

**path() argument: view**
When Django finds a matching pattern, it calls the specified view function with an HttpRequest object as the first argument and any “captured” values from the route as keyword arguments. We’ll give an example of this in a bit.

**path() argument: kwargs**
Arbitrary keyword arguments can be passed in a dictionary to the target view. We aren’t going to use this feature of Django in the tutorial.

**path() argument: name**
Naming your URL lets you refer to it unambiguously `(not open to more than one interpretation.)` from elsewhere in Django, especially from within templates. This powerful feature allows you to make global changes to the URL patterns of your project while only touching a single file.

> **Where to get help:** If you’re having trouble going through this tutorial, please head over to the [Getting Help](https://docs.djangoproject.com/en/3.2/faq/help/) section of the FAQ.

## Database Setup

Now, open up **mysite/settings.py.** It’s a normal Python module with module-level variables representing Django settings.

By default, the configuration uses **SQLite.** If you’re new to databases, or you’re just interested in trying Django, this is the easiest choice. SQLite is included in Python, so you won’t need to install anything else to support your database. When starting your first real project, however, you may want to use a more scalable database like PostgreSQL, to avoid database-switching headaches down the road.

If you wish to use another database, install the appropriate database bindings and change the following keys in the **DATABASES 'default'** item to match your database connection settings:

- **ENGINE** – Either **'django.db.backends.sqlite3'**, **'django.db.backends.postgresql'**, 'django.db.backends.mysql', or 'django.db.backends.oracle'. Other backends are also available.
- NAME – The name of your database. If you’re using SQLite, the database will be a file on your computer; in that case, **NAME** should be the full absolute path, including filename, of that file. The default value, **BASE_DIR / 'db.sqlite3'**, will store the file in your project directory.

If you are not using SQLite as your database, additional settings such as **USER, PASSWORD,** and **HOST** must be added. For more details, see the reference documentation for **DATABASES.**

> ***For databases other than SQLite:*** If you’re using a database besides SQLite, make sure you’ve created a database by this point. Do that with “CREATE DATABASE database_name;” within your database’s interactive prompt.
Also make sure that the database user provided in mysite/settings.py has “create database” privileges. This allows automatic creation of a test database which will be needed in a later tutorial.
If you’re using SQLite, you don’t need to create anything beforehand - the database file will be created automatically when it is needed.

While you’re editing mysite/settings.py, set TIME_ZONE to your time zone.

Also, note the **INSTALLED_APPS** setting at the top of the file. That holds the names of all Django applications that are activated in this Django instance. Apps can be used in multiple projects, and you can package and distribute them for use by others in their projects.

By default, **INSTALLED_APPS** contains the following apps, all of which come with Django:

- *django.contrib.admin* – The admin site. You’ll use it shortly.
- *django.contrib.auth* – An authentication system.
- *django.contrib.contenttypes* – A framework for content types.
- *django.contrib.sessions* – A session framework.
- *django.contrib.messages* – A messaging framework.
- *django.contrib.staticfiles* – A framework for managing static files.

These applications are included by default as a convenience for the common case.

Some of these applications make use of at least one database table, though, so we need to create the tables in the database before we can use them. To do that, run the following command: **`python3 manage.py migrate`**

The migrate command looks at the **INSTALLED_APPS** setting and creates any necessary database tables according to the database settings in your **mysite/settings.py** file and the database migrations shipped with the app (we’ll cover those later). You’ll see a message for each migration it applies. If you’re interested, run the command-line client for your database and type \dt (PostgreSQL), **SHOW TABLES**; (MariaDB, MySQL), **.schema** (SQLite), or S**ELECT TABLE_NAME FROM USER_TABLES; (Oracle)** to display the tables Django created.

> **For the minimalists**: Like we said above, the default applications are included for the common case, but not everybody needs them. If you don’t need any or all of them, feel free to comment-out or delete the appropriate line(s) from INSTALLED_APPS before running migrate. The migrate command will only run migrations for apps in INSTALLED_APPS.

## Creating Models

Now we’ll define your models – essentially, your database layout, with additional metadata.

> **Philosophy**: A model is the single, definitive source of truth about your data. It contains the essential fields and behaviors of the data you’re storing. Django follows the DRY Principle. The goal is to define your data model in one place and automatically derive things from it.
This includes the migrations - unlike in Ruby On Rails, for example, migrations are entirely derived from your models file, and are essentially a history that Django can roll through to update your database schema to match your current models.

In our poll app, we’ll create two models: Question and Choice. A Question has a question and a publication date. A Choice has two fields: the text of the choice and a vote tally. Each Choice is associated with a Question.

These concepts are represented by Python classes. Edit the polls/models.py file so it looks like this:

    polls/models.py
    from django.db import models

    class Question(models.Model):
        question_text = models.CharField(max_length=200)
        pub_date = models.DateTimeField('date published')
    
    class Choice(models.Model):
        question = models.ForeignKey(Question, on_delete=models.CASCADE)
        choice_text = models.CharField(max_length=200)
        votes = models.IntegerField(default=0)

Here, each model is represented by a class that subclasses django.db.models.Model. Each model has a number of class variables, each of which represents a database field in the model.

Each field is represented by an instance of a Field class – e.g., CharField for character fields and DateTimeField for datetimes. This tells Django what type of data each field holds.

The name of each Field instance (e.g. question_text or pub_date) is the field’s name, in machine-friendly format. You’ll use this value in your Python code, and your database will use it as the column name.

You can use an optional first positional argument to a Field to designate a human-readable name. That’s used in a couple of introspective parts of Django, and it doubles as documentation. If this field isn’t provided, Django will use the machine-readable name. In this example, we’ve only defined a human-readable name for Question.pub_date. For all other fields in this model, the field’s machine-readable name will suffice as its human-readable name.

Some Field classes have required arguments. CharField, for example, requires that you give it a max_length. That’s used not only in the database schema, but in validation, as we’ll soon see.

A Field can also have various optional arguments; in this case, we’ve set the default value of votes to 0.

Finally, note a relationship is defined, using ForeignKey. That tells Django each Choice is related to a single Question. Django supports all the common database relationships: many-to-one, many-to-many, and one-to-one.

## Basic Steps as follows

- python3 -m venv venv
- cd to venv
- pip3 install django(package)
- django-admin startproject (name of project)
- cd to project
- python3 manage.py startapp (name of app)
- cd to app directory
- create a new file in cd prompt. touch urls.py and add below details

        polls/urls.py
        from django.urls import path

        from polls import views
        urlpatterns = [
            path("", views.index, name="index")
        ]
- The next step is to point the root URLconf at the polls.urls module. In mysite/urls.py, add an import for django.urls.include and insert an include() in the urlpatterns list, so you have:

        mysite/urls.py
        from django.contrib import admin
        from django.urls import include, path

        urlpatterns = [
            path('polls/', include('polls.urls')),
            path('admin/', admin.site.urls),
        ]
- configure the databse you want to use. By default Sqlite3 is installed by django.
- Change Time Zone in settings: in place of UTC to change to India use **'Asia/Kolkata'**
- Next step: migrate data with this command. **`python3 manage.py migrate`**
- followed by **`python3 manage.py makemigrations`**
- Create Models in models.py file refer detail steps
