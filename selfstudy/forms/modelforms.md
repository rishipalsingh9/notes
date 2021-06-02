# Creating Forms from Models

## ModelForm

If you’re building a database-driven app, chances are you’ll have forms that map closely to Django models. For instance, you might have a BlogComment model, and you want to create a form that lets people submit comments. In this case, it would be redundant to define the field types in your form, because you’ve already defined the fields in your model.

For this reason, Django provides a helper class that lets you create a Form class from a Django model.

For example:

    >>> from django.forms import ModelForm
    >>> from myapp.models import Article

    # Create the form class.
    >>> class ArticleForm(ModelForm):
    ...     class Meta:
    ...         model = Article
    ...         fields = ['pub_date', 'headline', 'content', 'reporter']

    # Creating a form to add an article.
    >>> form = ArticleForm()

    # Creating a form to change an existing article.
    >>> article = Article.objects.get(pk=1)
    >>> form = ArticleForm(instance=article)

### Field Types

The generated Form class will have a form field for every model field specified, in the order specified in the fields attribute.

Each model field has a corresponding default form field. For example, a CharField on a model is represented as a CharField on a form. A model ManyToManyField is represented as a MultipleChoiceField. Here is the full list of conversions:
[Click on link to find](https://docs.djangoproject.com/en/3.2/topics/forms/modelforms/#considerations-regarding-model-s-error-messages)

As you might expect, the ForeignKey and ManyToManyField model field types are special cases:

- ForeignKey is represented by django.forms.ModelChoiceField, which is a ChoiceField whose choices are a model QuerySet.
- ManyToManyField is represented by django.forms.ModelMultipleChoiceField, which is a MultipleChoiceField whose choices are a model QuerySet.

In addition, each generated form field has attributes set as follows:

- If the model field has blank=True, then required is set to False on the form field. Otherwise, required=True.
- The form field’s label is set to the verbose_name of the model field, with the first character capitalized.
- The form field’s help_text is set to the help_text of the model field.
- If the model field has choices set, then the form field’s widget will be set to Select, with choices coming from the model field’s choices. The choices will normally include the blank choice which is selected by default. If the field is required, this forces the user to make a selection. The blank choice will not be included if the model field has blank=False and an explicit default value (the default value will be initially selected instead).

Finally, note that you can override the form field used for a given model field. See Overriding the default fields below. Overriding will be discussed in the next coming points.

### A Full Example

Consider this set of models:

    from django.db import models
    from django.forms import ModelForm

    TITLE_CHOICES = [
        ('MR', 'Mr.'),
        ('MRS', 'Mrs.'),
        ('MS', 'Ms.'),
    ]

    class Author(models.Model):
        name = models.CharField(max_length=100)
        title = models.CharField(max_length=3, choices=TITLE_CHOICES)
        birth_date = models.DateField(blank=True, null=True)

        def __str__(self):
            return self.name

    class Book(models.Model):
        name = models.CharField(max_length=100)
        authors = models.ManyToManyField(Author)

    class AuthorForm(ModelForm):
        class Meta:
            model = Author
            fields = ['name', 'title', 'birth_date']

    class BookForm(ModelForm):
        class Meta:
            model = Book
            fields = ['name', 'authors']

### Validation on a ModelForm

There are two main steps involved in validating a ModelForm:

1. [Validating the form](https://docs.djangoproject.com/en/3.2/ref/forms/validation/)
2. [Validating the model instance](https://docs.djangoproject.com/en/3.2/ref/models/instances/#validating-objects)

Just like normal form validation, model form validation is triggered implicitly when calling is_valid() or accessing the errors attribute and explicitly when calling full_clean(), although you will typically not use the latter method in practice.

Model validation (Model.full_clean()) is triggered from within the form validation step, right after the form’s clean() method is called.

>*Warning:*
The cleaning process modifies the model instance passed to the ModelForm constructor in various ways. For instance, any date fields on the model are converted into actual date objects. Failed validation may leave the underlying model instance in an inconsistent state and therefore it’s not recommended to reuse it.

### Overriding the clean() method

You can override the clean() method on a model form to provide additional validation in the same way you can on a normal form.

A model form instance attached to a model object will contain an instance attribute that gives its methods access to that specific model instance.

>*Warning:*
The ModelForm.clean() method sets a flag that makes the model validation step validate the uniqueness of model fields that are marked as unique, unique_together or unique_for_date|month|year.
If you would like to override the clean() method and maintain this validation, you must call the parent class’s clean() method.

### Interaction with model validation

As part of the validation process, ModelForm will call the clean() method of each field on your model that has a corresponding field on your form. If you have excluded any model fields, validation will not be run on those fields. See the form validation documentation for more on how field cleaning and validation work.

The model’s clean() method will be called before any uniqueness checks are made. See Validating objects for more information on the model’s clean() hook.

### Considerations regarding model’s error_messages

Error messages defined at the form field level or at the form Meta level always take precedence over the error messages defined at the model field level.

Error messages defined on model fields are only used when the ValidationError is raised during the model validation step and no corresponding error messages are defined at the form level.

You can override the error messages from NON_FIELD_ERRORS raised by model validation by adding the NON_FIELD_ERRORS key to the error_messages dictionary of the ModelForm’s inner Meta class:

from django.core.exceptions import NON_FIELD_ERRORS
from django.forms import ModelForm

    class ArticleForm(ModelForm):
        class Meta:
            error_messages = {
                NON_FIELD_ERRORS: {
                    'unique_together': "%(model_name)s's %(field_labels)s are not unique.",
                }

### THE SAVE()METHOD

Every ModelForm also has a save() method. This method creates and saves a database object from the data bound to the form. A subclass of ModelForm can accept an existing model instance as the keyword argument instance; if this is supplied, save() will update that instance. If it’s not supplied, save() will create a new instance of the specified model:

    >>> from myapp.models import Article
    >>> from myapp.forms import ArticleForm

    # Create a form instance from POST data.
    >>> f = ArticleForm(request.POST)

    # Save a new Article object from the form's data.
    >>> new_article = f.save()

    # Create a form to edit an existing Article, but use
    # POST data to populate the form.
    >>> a = Article.objects.get(pk=1)
    >>> f = ArticleForm(request.POST, instance=a)
    >>> f.save()

Note that if the form hasn’t been validated, calling save() will do so by checking form.errors. A ValueError will be raised if the data in the form doesn’t validate – i.e., if form.errors evaluates to True.

If an optional field doesn’t appear in the form’s data, the resulting model instance uses the model field default, if there is one, for that field. This behavior doesn’t apply to fields that use CheckboxInput, CheckboxSelectMultiple, or SelectMultiple (or any custom widget whose value_omitted_from_data() method always returns False) since an unchecked checkbox and unselected `<select multiple>` don’t appear in the data of an HTML form submission. Use a custom form field or widget if you’re designing an API and want the default fallback behavior for a field that uses one of these widgets.

This save() method accepts an optional commit keyword argument, which accepts either True or False. If you call save() with commit=False, then it will return an object that hasn’t yet been saved to the database. In this case, it’s up to you to call save() on the resulting model instance. This is useful if you want to do custom processing on the object before saving it, or if you want to use one of the specialized model saving options. commit is True by default.

Another side effect of using commit=False is seen when your model has a many-to-many relation with another model. If your model has a many-to-many relation and you specify commit=False when you save a form, Django cannot immediately save the form data for the many-to-many relation. This is because it isn’t possible to save many-to-many data for an instance until the instance exists in the database.

To work around this problem, every time you save a form using commit=False, Django adds a save_m2m() method to your ModelForm subclass. After you’ve manually saved the instance produced by the form, you can invoke save_m2m() to save the many-to-many form data. For example:

    # Create a form instance with POST data.
    >>> f = AuthorForm(request.POST)

    # Create, but don't save the new author instance.
    >>> new_author = f.save(commit=False)

    # Modify the author in some way.
    >>> new_author.some_field = 'some_value'

    # Save the new instance.
    >>> new_author.save()

    # Now, save the many-to-many data for the form.
    >>> f.save_m2m()

Calling save_m2m() is only required if you use save(commit=False). When you use a save() on a form, all data – including many-to-many data – is saved without the need for any additional method calls. For example:

    # Create a form instance with POST data.
    >>> a = Author()
    >>> f = AuthorForm(request.POST, instance=a)

    # Create and save the new author instance. There's no need to do anything else.
    >>> new_author = f.save()

Other than the save() and save_m2m() methods, a ModelForm works exactly the same way as any other forms form. For example, the is_valid() method is used to check for validity, the is_multipart() method is used to determine whether a form requires multipart file upload (and hence whether request.FILES must be passed to the form), etc. See Binding uploaded files to a form for more information.
