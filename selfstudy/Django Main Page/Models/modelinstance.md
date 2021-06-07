# Model Instance Reference

This document describes the details of the Model API. It builds on the material presented in the [model](models.md) and [database query guides](queryset.md), so you’ll probably want to read and understand those documents before reading this one.

Throughout this reference we’ll use the [example Weblog models](queryset) presented in the database query guide.

## Creating Objects

To create a new instance of a model, instantiate it like any other Python class:

### class Model(`**`*kwargs*)

The keyword arguments are the names of the fields you’ve defined on your model. Note that instantiating a model in no way touches your database; for that, you need to save().

>**Note:**
You may be tempted to customize the model by overriding the `__init__` method. If you do so, however, take care not to change the calling signature as any change may prevent the model instance from being saved. Rather than overriding `__init__`, try using one of these approaches:

1. Add a classmethod on the model class:

    from django.db import models

    class Book(models.Model):
        title = models.CharField(max_length=100)

        @classmethod
        def create(cls, title):
            book = cls(title=title)
            # do something with the book
            return book

    book = Book.create("Pride and Prejudice")

2. Add a method on a custom manager (usually preferred):

    class BookManager(models.Manager):
        def create_book(self, title):
            book = self.create(title=title)
            # do something with the book
            return book

    class Book(models.Model):
        title = models.CharField(max_length=100)

        objects = BookManager()

    book = Book.objects.create_book("Pride and Prejudice")

## Customizing Model Loading

### classmethod Model.from_db(db, field_names, values)

The from_db() method can be used to customize model instance creation when loading from the database.

The db argument contains the database alias for the database the model is loaded from, field_names contains the names of all loaded fields, and values contains the loaded values for each field in field_names. The field_names are in the same order as the values. If all of the model’s fields are present, then values are guaranteed to be in the order `__init__()` expects them. That is, the instance can be created by cls(*values). If any fields are deferred, they won’t appear in field_names. In that case, assign a value of django.db.models.DEFERRED to each of the missing fields.

In addition to creating the new model, the `from_db() method must set the adding and db flags in the new instance’s _state` attribute.

Below is an example showing how to record the initial values of fields that are loaded from the database:

    from django.db.models import DEFERRED

    @classmethod
    def from_db(cls, db, field_names, values):
        # Default implementation of from_db() (subject to change and could
        # be replaced with super()).
        if len(values) != len(cls._meta.concrete_fields):
            values = list(values)
            values.reverse()
            values = [
                values.pop() if f.attname in field_names else DEFERRED
                for f in cls._meta.concrete_fields
            ]
        instance = cls(*values)
        instance._state.adding = False
        instance._state.db = db
        # customization to store the original field values on the instance
        instance._loaded_values = dict(zip(field_names, values))
        return instance

    def save(self, *args, **kwargs):
        # Check how the current values differ from ._loaded_values. For example,
        # prevent changing the creator_id of the model. (This example doesn't
        # support cases where 'creator_id' is deferred).
        if not self._state.adding and (
                self.creator_id != self._loaded_values['creator_id']):
            raise ValueError("Updating the value of creator isn't allowed")
        super().save(*args, **kwargs)

The example above shows a full from_db() implementation to clarify how that is done. In this case it would be possible to use a super() call in the from_db() method.
