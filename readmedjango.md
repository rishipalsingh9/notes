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

Finally, note a relationship is defined, using **[ForeignKey](https://docs.djangoproject.com/en/3.2/ref/models/fields/#django.db.models.ForeignKey)**. That tells Django each Choice is related to a single Question. Django supports all the common database relationships: many-to-one, many-to-many, and one-to-one.

### Activating Models

That small bit of model code gives Django a lot of information. With it, Django is able to:

- Create a database schema (CREATE TABLE statements) for this app.
- Create a Python database-access API for accessing Question and Choice objects.

But first we need to tell our project that the polls app is installed.

> **Philosophy**: Django apps are “pluggable”: You can use an app in multiple projects, and you can distribute apps, because they don’t have to be tied to a given Django installation.
>****

To include the app in our project, we need to add a reference to its configuration class in the INSTALLED_APPS setting. The PollsConfig class is in the polls/apps.py file, so its dotted path is 'polls.apps.PollsConfig'. Edit the mysite/settings.py file and add that dotted path to the INSTALLED_APPS setting. It’ll look like this:

    mysite/settings.py
    
    INSTALLED_APPS = [
    'polls.apps.PollsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    ]

Now Django knows to include the polls app. Let’s run another command:

**`python3 manage.py makemigrations polls`**

By running makemigrations, you’re telling Django that you’ve made some changes to your models (in this case, you’ve made new ones) and that you’d like the changes to be stored as a migration.

Migrations are how Django stores changes to your models (and thus your database schema) - they’re files on disk. You can read the migration for your new model if you like; it’s the file polls/migrations/0001_initial.py. Don’t worry, you’re not expected to read them every time Django makes one, but they’re designed to be human-editable in case you want to manually tweak how Django changes things.

There’s a command that will run the migrations for you and manage your database schema automatically - that’s called migrate, and we’ll come to it in a moment - but first, let’s see what SQL that migration would run. The sqlmigrate command takes migration names and returns their SQL:

**`python manage.py sqlmigrate polls 0001`**

You should see something similar to the following (we’ve reformatted it for readability):

    BEGIN;
    --
    -- Create model Question
    --
    CREATE TABLE "polls_question" (
        "id" serial NOT NULL PRIMARY KEY,
        "question_text" varchar(200) NOT NULL,
        "pub_date" timestamp with time zone NOT NULL
    );
    --
    -- Create model Choice
    --
    CREATE TABLE "polls_choice" (
        "id" serial NOT NULL PRIMARY KEY,
        "choice_text" varchar(200) NOT NULL,
        "votes" integer NOT NULL,
        "question_id" integer NOT NULL
    );
    ALTER TABLE "polls_choice"
    ADD CONSTRAINT "polls_choice_question_id_c5b4b260_fk_polls_question_id"
        FOREIGN KEY ("question_id")
        REFERENCES "polls_question" ("id")
        DEFERRABLE INITIALLY DEFERRED;
    CREATE INDEX "polls_choice_question_id_c5b4b260" ON "polls_choice" ("question_id");
    
    COMMIT;

Note the following:

- The exact output will vary depending on the database you are using. The example above is generated for PostgreSQL.
- Table names are automatically generated by combining the name of the app (polls) and the lowercase name of the model – question and choice. (You can override this behavior.)
- Primary keys (IDs) are added automatically. (You can override this, too.)
- By convention, Django appends "_id" to the foreign key field name. (Yes, you can override this, as well.)
- The foreign key relationship is made explicit by a FOREIGN KEY constraint. Don’t worry about the DEFERRABLE parts; it’s telling PostgreSQL to not enforce the foreign key until the end of the transaction.
- It’s tailored to the database you’re using, so database-specific field types such as auto_increment (MySQL), serial (PostgreSQL), or integer primary key autoincrement (SQLite) are handled for you automatically. Same goes for the quoting of field names – e.g., using double quotes or single quotes.
- The sqlmigrate command doesn’t actually run the migration on your database - instead, it prints it to the screen so that you can see what SQL Django thinks is required. It’s useful for checking what Django is going to do or if you have database administrators who require SQL scripts for changes.

If you’re interested, you can also run python manage.py check; this checks for any problems in your project without making migrations or touching the database.

The migrate command takes all the migrations that haven’t been applied (Django tracks which ones are applied using a special table in your database called django_migrations) and runs them against your database - essentially, synchronizing the changes you made to your models with the schema in the database.

Migrations are very powerful and let you change your models over time, as you develop your project, without the need to delete your database or tables and make new ones - it specializes in upgrading your database live, without losing data. We’ll cover them in more depth in a later part of the tutorial, but for now, remember the three-step guide to making model changes:

- Change your models (in models.py).
- Run python manage.py makemigrations to create migrations for those changes
- Run python manage.py migrate to apply those changes to the database.

The reason that there are separate commands to make and apply migrations is because you’ll commit migrations to your version control system and ship them with your app; they not only make your development easier, they’re also usable by other developers and in production.

Read the [django-admin documentation](https://docs.djangoproject.com/en/3.2/ref/django-admin/) for full information on what the manage.py utility can do.

### Playing with the API

Now, let’s hop into the interactive Python shell and play around with the free API Django gives you. To invoke the Python shell, use this command:

**`python manage.py shell`**

We’re using this instead of simply typing “python”, because manage.py sets the DJANGO_SETTINGS_MODULE environment variable, which gives Django the Python import path to your mysite/settings.py file.

Once you’re in the shell, explore the database API:

        >>> from polls.models import Choice, Question  # Import the model classes we just wrote.

        # No questions are in the system yet.
        >>> Question.objects.all()
        <QuerySet []>

        # Create a new Question.
        # Support for time zones is enabled in the default settings file, so
        # Django expects a datetime with tzinfo for pub_date. Use timezone.now()
        # instead of datetime.datetime.now() and it will do the right thing.
        >>> from django.utils import timezone
        >>> q = Question(question_text="What's new?", pub_date=timezone.now())

        # Save the object into the database. You have to call save() explicitly.
        >>> q.save()

        # Now it has an ID.
        >>> q.id
        1

        # Access model field values via Python attributes.
        >>> q.question_text
        "What's new?"
        >>> q.pub_date
        datetime.datetime(2012, 2, 26, 13, 0, 0, 775217, tzinfo=<UTC>)

        # Change values by changing the attributes, then calling save().
        >>> q.question_text = "What's up?"
        >>> q.save()

        # objects.all() displays all the questions in the database.
        >>> Question.objects.all()
        <QuerySet [<Question: Question object (1)>]>

Wait a minute. <Question: Question object (1)> isn’t a helpful representation of this object. Let’s fix that by editing the Question model (in the polls/models.py file) and adding a __str__() method to both Question and Choice:

        polls/models.py
        from django.db import models

        class Question(models.Model):
            # ...
            def __str__(self):
                return self.question_text

        class Choice(models.Model):
            # ...
            def __str__(self):
                return self.choice_text

It’s important to add __str__() methods to your models, not only for your own convenience when dealing with the interactive prompt, but also because objects’ representations are used throughout Django’s automatically-generated admin.

Let’s also add a custom method to this model:

        polls/models.py

        import datetime

        from django.db import models
        from django.utils import timezone


        class Question(models.Model):
            # ...
            def was_published_recently(self):
                return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

Note the addition of import datetime and from django.utils import timezone, to reference Python’s standard datetime module and Django’s time-zone-related utilities in django.utils.timezone, respectively. If you aren’t familiar with time zone handling in Python, you can learn more in the time zone support docs.

Save these changes and start a new Python interactive shell by running python manage.py shell again:

For more information on model relations, see [Accessing related objects.](https://docs.djangoproject.com/en/3.2/ref/models/relations/) For more on how to use double underscores to perform field lookups via the API, see [Field lookups.](https://docs.djangoproject.com/en/3.2/topics/db/queries/#field-lookups-intro) For full details on the database API, see our [Database API reference.](https://docs.djangoproject.com/en/3.2/topics/db/queries/)

## Introducing the Django Admin

> **Philosphy**: Generating admin sites for your staff or clients to add, change, and delete content is tedious work that doesn’t require much creativity. For that reason, Django entirely automates creation of admin interfaces for models.
Django was written in a newsroom environment, with a very clear separation between “content publishers” and the “public” site. Site managers use the system to add news stories, events, sports scores, etc., and that content is displayed on the public site. Django solves the problem of creating a unified interface for site administrators to edit content.
The admin isn’t intended to be used by site visitors. It’s for site managers.

### Creating an admin user

First we’ll need to create a user who can login to the admin site. Run the following command:

**`python manage.py createsuperuser`**

### Make the poll app modifiable in the admin

But where’s our poll app? It’s not displayed on the admin index page.

Only one more thing to do: we need to tell the admin that Question objects have an admin interface. To do this, open the polls/admin.py file, and edit it to look like this:

    polls/admin.py
    from django.contrib import admin

    from .models import Question

    admin.site.register(Question)

## Overview

A view is a “type” of Web page in your Django application that generally serves a specific function and has a specific template. For example, in a blog application, you might have the following views:

- Blog homepage – displays the latest few entries.
- Entry “detail” page – permalink page for a single entry.
- Year-based archive page – displays all months with entries in the given year.
- Month-based archive page – displays all days with entries in the given month.
- Day-based archive page – displays all entries in the given day.
- Comment action – handles posting comments to a given entry.

In our poll application, we’ll have the following four views:

- Question “index” page – displays the latest few questions.
- Question “detail” page – displays a question text, with no results but with a form to vote.
- Question “results” page – displays results for a particular question.
- Vote action – handles voting for a particular choice in a particular question.

In Django, web pages and other content are delivered by views. Each view is represented by a Python function (or method, in the case of class-based views). Django will choose a view by examining the URL that’s requested (to be precise, the part of the URL after the domain name).

Now in your time on the web you may have come across such beauties as ME2/Sites/dirmod.htm?sid=&type=gen&mod=Core+Pages&gid=A6CD4967199A42D9B65B1B. You will be pleased to know that Django allows us much more elegant URL patterns than that.

A URL pattern is the general form of a URL - for example: /newsarchive/<year>/<month>/.

To get from a URL to a view, Django uses what are known as ‘URLconfs’. A URLconf maps URL patterns to views.

This tutorial provides basic instruction in the use of URLconfs, and you can refer to [URL dispatcher](https://docs.djangoproject.com/en/3.2/topics/http/urls/) for more information.

### Writing more views

Now let’s add a few more views to **polls/views.py.** These views are slightly different, because they take an argument:

    def detail(request, question_id):
        return HttpResponse("You're looking at question %s." % question_id)

    def results(request, question_id):
        response = "You're looking at the results of question %s."
        return HttpResponse(response % question_id)

    def vote(request, question_id):
        return HttpResponse("You're voting on question %s." % question_id)

Take a look in your browser, at “/polls/34/”. It’ll run the detail() method and display whatever ID you provide in the URL. Try “/polls/34/results/” and “/polls/34/vote/” too – these will display the placeholder results and voting pages.

When somebody requests a page from your website – say, “/polls/34/”, Django will load the mysite.urls Python module because it’s pointed to by the ROOT_URLCONF setting. It finds the variable named urlpatterns and traverses the patterns in order. After finding the match at 'polls/', it strips off the matching text ("polls/") and sends the remaining text – "34/" – to the ‘polls.urls’ URLconf for further processing. There it matches `'<int:question_id>/'`, resulting in a call to the detail() view like so:

**`detail(request=<HttpRequest object>, question_id=34)`**

The question_id=34 part comes from <int:question_id>. Using angle brackets “captures” part of the URL and sends it as a keyword argument to the view function. The :question_id> part of the string defines the name that will be used to identify the matched pattern, and the `<int:` part is a converter that determines what patterns should match this part of the URL path.

### Write views that actually do something

Each view is responsible for doing one of two things: returning an HttpResponse object containing the content for the requested page, or raising an exception such as Http404. The rest is up to you.

Your view can read records from a database, or not. It can use a template system such as Django’s – or a third-party Python template system – or not. It can generate a PDF file, output XML, create a ZIP file on the fly, anything you want, using whatever Python libraries you want.

All Django wants is that HttpResponse. Or an exception.

Because it’s convenient, let’s use Django’s own database API, which we covered in Tutorial 2. Here’s one stab at a new index() view, which displays the latest 5 poll questions in the system, separated by commas, according to publication date:

    polls/views.py

    from django.http import HttpResponse

    from .models import Question

    def index(request):
        latest_question_list = Question.objects.order_by('-pub_date')[:5]
        output = ', '.join([q.question_text for q in latest_question_list])
        return HttpResponse(output)
    
    #Leave the rest of the views (detail, results, vote) unchanged

There’s a problem here, though: the page’s design is hard-coded in the view. If you want to change the way the page looks, you’ll have to edit this Python code. So let’s use Django’s template system to separate the design from Python by creating a template that the view can use.

First, create a directory called templates in your polls directory. Django will look for templates in there.

Your project’s TEMPLATES setting describes how Django will load and render templates. The default settings file configures a DjangoTemplates backend whose APP_DIRS option is set to True. By convention DjangoTemplates looks for a “templates” subdirectory in each of the INSTALLED_APPS.

Within the templates directory you have just created, create another directory called polls, and within that create a file called index.html. In other words, your template should be at polls/templates/polls/index.html. Because of how the app_directories template loader works as described above, you can refer to this template within Django as polls/index.html.

> **Template Namespacing:** Now we might be able to get away with putting our templates directly in polls/templates (rather than creating another polls subdirectory), but it would actually be a bad idea. Django will choose the first template it finds whose name matches, and if you had a template with the same name in a different application, Django would be unable to distinguish between them. We need to be able to point Django at the right one, and the best way to ensure this is by namespacing them. That is, by putting those templates inside another directory named for the application itself.

Put the following code in that template:

    polls/templates/polls/index.html

    {% if latest_question_list %}
    <ul>
        {% for question in latest_question_list %}
            <li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
        {% endfor %}
    </ul>
    {% else %}
        <p>No polls are available.</p>
    {% endif %}

> **Note:** To make the tutorial shorter, all template examples use incomplete HTML. In your own projects you should use [complete HTML documents](https://developer.mozilla.org/en-US/docs/Learn/HTML/Introduction_to_HTML/Getting_started#anatomy_of_an_html_document)

Now let’s update our index view in polls/views.py to use the template:

    polls/views.py
    from django.http import HttpResponse
    from django.template import loader

    from .models import Question
    def index(request):
        latest_question_list = Question.objects.order_by('-pub_date')[:5]
        template = loader.get_template('polls/index.html')
        context = {
            'latest_question_list': latest_question_list,
        }
    return HttpResponse(template.render(context, request))

That code loads the template called polls/index.html and passes it a context. The context is a dictionary mapping template variable names to Python objects.

Load the page by pointing your browser at “/polls/”, and you should see a bulleted-list containing the “What’s up” question from Tutorial 2. The link points to the question’s detail page.

### A shortcut: render() 

It’s a very common idiom to load a template, fill a context and return an HttpResponse object with the result of the rendered template. Django provides a shortcut. Here’s the full index() view, rewritten:

    polls/views.py

    from django.shortcuts import render

    from .models import Question

    def index(request):
        latest_question_list = Question.objects.order_by('-pub_date')[:5]
        context = {'latest_question_list': latest_question_list}
        return render(request, 'polls/index.html', context)

Note that once we’ve done this in all these views, we no longer need to import loader and HttpResponse (you’ll want to keep HttpResponse if you still have the stub methods for detail, results, and vote).

The render() function takes the request object as its first argument, a template name as its second argument and a dictionary as its optional third argument. It returns an HttpResponse object of the given template rendered with the given context.

### Raising a 404 error

Now, let’s tackle the question detail view – the page that displays the question text for a given poll. Here’s the view:

    polls/views.py
    from django.http import Http404
    from django.shortcuts import render

    from .models import Question
    # ...
    def detail(request, question_id):
        try:
            question = Question.objects.get(pk=question_id)
        except Question.DoesNotExist:
            raise Http404("Question does not exist")
        return render(request, 'polls/detail.html', {'question': question})


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
- If you want to check if everything is fine before migrate command use this command. **`python manage.py check`**
- Next step: migrate data with this command. **`python3 manage.py migrate`**
- followed by **`python3 manage.py makemigrations`**
- Create Models in models.py file refer detail steps
- Settings.py add your app as the app name in installed apps list.
- To link Foreign_key to primary mention after cascade(primary_key=True).
- Create Template folder in polls directory. In template folder create polls and then index.html.. poll/templates/polls/index.html

- 