# Django 3.2 Documentation

## The Model Layer

Django provides an abstraction layer (the “models”) for structuring and manipulating the data of your Web application. Learn more about it below:

Models have below pages to lookout

- Introduction to Models
- QuerySets (Important to select data from the Database)
- Aggregate - shortcut query sets
- Search - To make searches in Databases 
- Managers - interface through which db query are provided to Django.

- **[Models](Models/models.md)**: Introduction to models | Field types | Indexes | Meta options | Model class | Choices | Help_Text | Extend Models from another App
- **[QuerySets](Models/queryset.md)**: Making queries | QuerySet method reference | Lookup expressions.
- **[Model Instances](Models/modelinstance.md)**: Instance methods | Accessing related objects.
- **[Migrations](Models/migrations.md)**: Introduction to Migrations | Operations reference | SchemaEditor | Writing migrations.
- **[Advanced](Models/advanced.md)**: Managers | Raw SQL | Transactions | Aggregation | Search | Custom fields | Multiple databases | Custom lookups | Query Expressions | Conditional - Expressions | Database Functions.
- **[Other](Models/other.md)**: Supported databases | Legacy databases | Providing initial data | Optimize database access | PostgreSQL specific features.

## The View Layer

Django has the concept of “views” to encapsulate the logic responsible for processing a user’s request and for returning the response. Find all you need to know about views via the links below:

- **[The Basics](../Views/basics.md)**: URLconfs | View functions | Shortcuts | Decorators | Asynchronous Support
- **[Reference](../Views/reference.md)**: Built-in Views | Request/response objects | TemplateResponse objects
- **[File uploads](../Views/fileupl.md)**: Overview | File objects | Storage API | Managing files | Custom storage
- **[Class-Based Views](../Views/classbased.md)**: Overview | Built-in display views | Built-in editing views | Using mixins | API reference | Flattened index
- **[Advanced](../Views/advance.md)**: Generating CSV | Generating PDF
- **[Middleware](../Views/middleware.md)**: Overview | Built-in middleware classes

## The Template Layer

The template layer provides a designer-friendly syntax for rendering the information to be presented to the user. Learn how this syntax can be used by designers and how it can be extended by programmers:

- **[The basics: Overview](Templatelayer.md/basic.md)**
- **[For designers](Templatelayer.md/for_designers.md)**: Language overview | Built-in tags and filters | Humanization
- **[For programmers](Templatelayer.md/for_programmers.md)**: Template API | Custom tags and filters | Custom template backend

## Forms

Django provides a rich framework to facilitate the creation of forms and the manipulation of form data.

- The basics: Overview | Form API | Built-in fields | Built-in widgets
- Advanced: Forms for models | Integrating media | Formsets | Customizing validation

## The development process

Learn about the various components and tools to help you in the development and testing of Django applications:

- Settings: Overview | Full list of settings
- Applications: Overview
- Exceptions: Overview
- django-admin and manage.py: Overview | Adding custom commands
- Testing: Introduction | Writing and running tests | - Included testing tools | Advanced topics
- Deployment: Overview | WSGI servers | ASGI servers | Deploying static files | Tracking code errors by email | Deployment checklist

## The Admin

Find all you need to know about the automated admin interface, one of Django’s most popular features:

- Admin site
- Admin actions
- Admin documentation generator

## Security

Security is a topic of paramount importance in the development of Web applications and Django provides multiple protection tools and mechanisms:

- Security overview
- Disclosed security issues in Django
- Clickjacking protection
- Cross Site Request Forgery protection
- Cryptographic signing
- Security Middleware

## Internationalization and localization

Django offers a robust internationalization and localization framework to assist you in the development of applications for multiple languages and world regions:

- Overview | Internationalization | Localization | Localized Web UI formatting and form input
- Time zones

## Performance and optimization

There are a variety of techniques and tools that can help get your code running more efficiently - faster, and using fewer system resources.

- Performance and optimization overview

## Geographic framework

GeoDjango intends to be a world-class geographic Web framework. Its goal is to make it as easy as possible to build GIS Web applications and harness the power of spatially enabled data.

## Common Web application tools

Django offers multiple tools commonly needed in the development of Web applications:

- Authentication: Overview | Using the authentication system | Password management | Customizing authentication | API Reference
- Caching
- Logging
- Sending emails
- Syndication feeds (RSS/Atom)
- Pagination
- Messages framework
- Serialization
- Sessions
- Sitemaps
- Static files management
- Data validation

## Other core functionalities

Learn about some other core functionalities of the Django framework:

- Conditional content processing
- Content types and generic relations
- Flatpages
- Redirects
- Signals
- System check framework
- The sites framework
- Unicode in Django

## The Django open-source project

Learn about the development process for the Django project itself and about how you can contribute:

- Community: How to get involved | The release process | Team organization | The Django source code repository | Security policies | Mailing lists
- Design philosophies: Overview
- Documentation: About this documentation
- Third-party distributions: Overview
- Django over time: API stability | Release notes and upgrading instructions | Deprecation Timeline
