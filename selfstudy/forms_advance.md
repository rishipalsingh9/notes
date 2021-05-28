# Self Study on Forms

## Form are unbound and Bound

A form instance is either a Bound to set a data or unbound.

- If its bound to set a data, its capable of validating the data and rendering the form as HTML with the data displayed in HTML.
- If it's unbound it cannot dp validation (because there's no data to validate!), but it can still render the blank form.

### *class* Form

To create an unbound Form instance, instantiate (represent as or by an instance) the class.

    >>> f = ContactForm()

To bind data to form pass data as dictionary as the first parameter to your Form class conductor.

    >>> data = {'subject': 'hello',
    ...         'message': 'Hi there',
    ...         'sender': 'foo@example.com',
    ...         'cc_myself': True}
    >>> f = ContactForm(data)

In this dictinary,

- the keys are the field names.
- which correspond to the attributes in your Form class.
- The values are the data you're trying to validate.
- These will usually be strings, but there's no requirement that they be strings; depends on the type of data you passed depends on the Field.

### Form.is_bound

If you want to distinguish between bound & unbound form instance in runtime, check the value of form.is_bound attribute:

    >>> f = ContactForm()
    >>> f.is_bound
    False
    >>> f = ContactForm({'subject': 'hello'})
    >>> f.is_bound
    True

> *Tip:* So the main difference of unbound is you pass data as dictionery and then save form which will do nothing. On the other hand bound form will do validation of data.

Note that passing an empty dictionary creates a bound form with empty data:

    >>> f = ContactForm({})
    >>> f.is_bound
    True

>*Note:* There is no way to change data in a Form instance. Once a Form instance has been created, you should consider its data ***immutable*** (unchanging over time or unable to be changed.), whether it has data or not.

## Using Forms to Validate Data

### Form.clean() - Method

Implement clean method on your form when you must add custom validation for the fields that are interdependent. [Cleaning and Validation fields dependent on each other](https://docs.djangoproject.com/en/3.2/ref/forms/validation/#validating-fields-with-clean)

### Form.is_valid() - Method

- Primary task is to validate data
- With a bound Form instance call for is_valid()
  - It will validate data
  - Run Boolean (true or false)

        >>> data = {'subject': 'hello',
        ...         'message': 'Hi there',
        ...         'sender': 'foo@example.com',
        ...         'cc_myself': True}
        >>> f = ContactForm(data)
        >>> f.is_valid()
        True

- if you enter invalid data below will be the (False) will be the boolean

        >>> data = {'subject': '',
        ...         'message': 'Hi there',
        ...         'sender': 'invalid email address',
        ...         'cc_myself': True}
        >>> f = ContactForm(data)
        >>> f.is_valid()
        False

### Form.errors - Method

Access the errors attribute to get a dictionary of error message

    >>> f.errors
    {'sender': ['Enter a valid email address.'], 'subject': ['This field is required.']}

- in this method you get the errors as mentioned above
- dont need to pass is_valid() method.
- form's data will be validated either you call errors or is_valid.
- if there is any errors it will be triggered in once.

### Form.errors.as_data() - Method

Returns a dict that maps fields to their original ValidationError instances.

    >>> f.errors.as_data()
    {'sender': [ValidationError(['Enter a valid email address.'])],
    'subject': [ValidationError(['This field is required.'])]}

- to identify error by its code.
- use anytime.
- enables to rewrite the error messages or writing custom logic views.
- seralize errors in custom formats (eg: XML) for instance, as_json() relies on as_data()
- need for this method due to backwards compatibility.
- ValidationError instances were lost as soon as their rendered error messages were added to the Form.errors dict,
- Ideally Form.errors would stored the same.

### Form.erros.as_json(escape_html=False)

- Returns errors serialized as JSON
- By default it doesn't escape its output.
- Good for avoiding cross-site scripting attack in case you are using AJAX requests form to view where client interprets the response.
- if you don't want to use client-side escaping then set (escape_html=True)

### Form.erros.get_json_data(escape_html=False)

Returns the errors as a dictionary suitable for serializing to JSON. Form.errors.as_json() returns serialized JSON, while this returns the error data before it’s serialized.

The escape_html parameter behaves as described in Form.errors.as_json().

### Form.add_error(field, error)

- This method allow adding error to specific field forms within the Form.clean() method or from outside.
- field argument is the name to which the error should be added.
- if its none it will be treated as non-field error.

## Dynamic Initial Values

### Form.initial

Use initial to declare the intial value of the form fields at runtime. Ex: you might want to fill username field of the current session. To accomplish this use the intial argument to a Form.

    >>> f = ContactForm(initial={'subject': 'Hi there!'})

If a field defines initial and you also included initial when instantiating the Form, then the latter initial will have precedence.
In below example it is mentioned in field level as well as form instance level, later will get precedence.

    >>> from django import forms
    >>> class CommentForm(forms.Form):
    ...     name = forms.CharField(initial='class')
    ...     url = forms.URLField()
    ...     comment = forms.CharField()
    >>> f = CommentForm(initial={'name': 'instance'}, auto_id=False)
    >>> print(f)
    <tr><th>Name:</th><td><input type="text" name="name" value="instance" required></td></tr>
    <tr><th>Url:</th><td><input type="url" name="url" required></td></tr>
    <tr><th>Comment:</th><td><input type="text" name="comment" required></td></tr>

### Form.get_initial_for_field(field, field_name)

- use this method to retrieve initial data for a form field.
- it retreives from Form.initial & Field.initial respectively and evaluates any callable initial values.

## Checking which form data has changed

### Form.has_changed()

- is used to check if the form data has been changed.
- returns bool value

        >>> data = {'subject': 'hello',
        ...         'message': 'Hi there',
        ...         'sender': 'foo@example.com',
        ...         'cc_myself': True}
        >>> f = ContactForm(data, initial=data)
        >>> f.has_changed()
        False

When the form is submitted, we reconstruct it and provides the original data so that comparision can be done.

    >>> f = ContactForm(request.POST, initial=data)
    >>> f.has_changed()

- will return True if data from request.POST differs from what was provided in initial or False otherwise.

### Form.changed_data

Returns the name of list which differs after request.POST from what was provided in initial. It returns empty list no data differs.

    >>> f = ContactForm(request.POST, initial=data)
    >>> if f.has_changed():
    ...     print("The following fields changed: %s" % ", ".join(f.changed_data))
    >>> f.changed_data
    ['subject', 'message']

## Accessing the fields from the Form

### Form.fields

You can access fields of the Form instance from its fields attribute:

    >>> for row in f.fields.values(): print(row)
    ...
    <django.forms.fields.CharField object at 0x7ffaac632510>
    <django.forms.fields.URLField object at 0x7ffaac632f90>
    <django.forms.fields.CharField object at 0x7ffaac3aa050>
    >>> f.fields['name']
    <django.forms.fields.CharField object at 0x7ffaac6324d0>

You can also alter the field of Form instance to change the way it is presented in the form.

    >>> f.as_table().split('\n')[0]
    '<tr><th>Name:</th><td><input name="name" type="text" value="instance" required></td></tr>'
    >>> f.fields['name'].label = "Username"
    >>> f.as_table().split('\n')[0]
    '<tr><th>Username:</th><td><input name="name" type="text" value="instance" required></td></tr>'

>***Beware:*** not to alter the base_fields attribute because this modification will influence all subsequesnt ContactForm instances within the Python process.

    >>> f.base_fields['name'].label = "Username"
    >>> another_f = CommentForm(auto_id=False)
    >>> another_f.as_table().split('\n')[0]
    '<tr><th>Username:</th><td><input name="name" type="text" value="class" required></td></tr>'

## Accessing "clean" data

### Form.cleaned_data

- is responsible for not only validating data as well as for "cleaning" it.
- it allows data of a particular field to input in variety of ways.

example of cleaned data as follows

    >>> data = {'subject': 'hello',
    ...         'message': 'Hi there',
    ...         'sender': 'foo@example.com',
    ...         'cc_myself': True}
    >>> f = ContactForm(data)
    >>> f.is_valid()
    True
    >>> f.cleaned_data
    {'cc_myself': True, 'message': 'Hi there', 'sender': 'foo@example.com', 'subject': 'hello'}

>*Note:* That every text field base such as Char or EmailField - always cleans the input into string.

- If data is not validated, the cleaned dict containes only the valid fields such as:

        >>> data = {'subject': '',
        ...         'message': 'Hi there',
        ...         'sender': 'invalid email address',
        ...         'cc_myself': True}
        >>> f = ContactForm(data)
        >>> f.is_valid()
        False
        >>> f.cleaned_data
        {'cc_myself': True, 'message': 'Hi there'}

- cleaned_data only contains the keys for fields defined in the Form.
  - In below example we are bunch of extra fields.

        >>> data = {'subject': 'hello',
        ...         'message': 'Hi there',
        ...         'sender': 'foo@example.com',
        ...         'cc_myself': True,
        ...         'extra_field_1': 'foo',
        ...         'extra_field_2': 'bar',
        ...         'extra_field_3': 'baz'}
        >>> f = ContactForm(data)
        >>> f.is_valid()
        True
        >>> f.cleaned_data # Doesn't contain extra_field_1, etc.
        {'cc_myself': True, 'message': 'Hi there', 'sender': 'foo@example.com', 'subject': 'hello'}

- when the form is valid, it will include key & value for all fields, even if data is not including value for some optional fields.

    Example as follows

        >>> from django import forms
        >>> class OptionalPersonForm(forms.Form):
        ...     first_name = forms.CharField()
        ...     last_name = forms.CharField()
        ...     nick_name = forms.CharField(required=False)
        >>> data = {'first_name': 'John', 'last_name': 'Lennon'}
        >>> f = OptionalPersonForm(data)
        >>> f.is_valid()
        True
        >>> f.cleaned_data
        {'nick_name': '', 'first_name': 'John', 'last_name': 'Lennon'}

In this above example, the cleaned_data value for nick_name is set to an empty string, because nick_name is CharField, and CharFields treat empty values as an empty string. Each field type knows what its “blank” value is – e.g., for DateField, it’s None instead of the empty string. For full details on each field’s behavior in this case, see the “Empty value” note for each field in the “Built-in Field classes” section below.

## Outputting Form as HTML

The second task of a Form object is to render itself as HTML. To do so, print it:

    >>> f = ContactForm()
    >>> print(f)
    <tr><th><label for="id_subject">Subject:</label></th><td><input id="id_subject" type="text" name="subject" maxlength="100" required></td></tr>
    <tr><th><label for="id_message">Message:</label></th><td><input type="text" name="message" id="id_message" required></td></tr>
    <tr><th><label for="id_sender">Sender:</label></th><td><input type="email" name="sender" id="id_sender" required></td></tr>
    <tr><th><label for="id_cc_myself">Cc myself:</label></th><td><input type="checkbox" name="cc_myself" id="id_cc_myself"></td></tr>

- if the form is bound to data, the HTML output will include that data appropriately.
- so if a field is represented by `<input type = text>`, the data will be in the value attribute.
- if field is represented by `<input type="checkbox">`, then data will include checked if appropriate:

        >>> data = {'subject': 'hello',
        ...         'message': 'Hi there',
        ...         'sender': 'foo@example.com',
        ...         'cc_myself': True}
        >>> f = ContactForm(data)
        >>> print(f)
        <tr><th><label for="id_subject">Subject:</label></th><td><input id="id_subject" type="text" name="subject" maxlength="100" value="hello" required></td></tr>
        <tr><th><label for="id_message">Message:</label></th><td><input type="text" name="message" id="id_message" value="Hi there" required></td></tr>
        <tr><th><label for="id_sender">Sender:</label></th><td><input type="email" name="sender" id="id_sender" value="foo@example.com" required></td></tr>
        <tr><th><label for="id_cc_myself">Cc myself:</label></th><td><input type="checkbox" name="cc_myself" id="id_cc_myself" checked></td></tr>

This default output is a two-column HTML table, with a `<tr>` for each field. Notice the following:

- for flexibilty, output doesnot include, `<table>`, `<form>` or `<input>` tags its your job to do so.
- Each field type has a default HTML representation
  - CharField represents as `<input type="text">`
  - EmailField represents as `<input type="email">`
  - BooleanField (null=False) represents as `<input type="checkbox">`
- These are the default settings, you can specify which HTML to use for a given field.
- The HTML name for each tag is taken directly from its attribute name in the ContactForm class.
- Each text label field - e.g. 'Subject:', 'Message:' & 'Cc myself:' is generated from the field name by converting all underscores and upper-casing first letter. These are defaults you can manually label them.
- Each text is surrounded in an HTML `<label>` tag, which points to field via its **id**. Its **id** & `<label>` tags are included in output by default, to follow best practices.
- The output uses HTML 5.

Although `<table>` output is the default output for forms when you print it. Each style is available as a method on a form object, and each rendering method returns a string.

## as_p()

### f.as_p() (form.as_p())

as_p() renders the form as a series of `<p>` tags, with each `<p>` containing one field:

    >>> f = ContactForm()
    >>> f.as_p()
    '<p><label for="id_subject">Subject:</label> <input id="id_subject" type="text" name="subject" maxlength="100" required></p>\n<p><label for="id_message">Message:</label> <input type="text" name="message" id="id_message" required></p>\n<p><label for="id_sender">Sender:</label> <input type="text" name="sender" id="id_sender" required></p>\n<p><label for="id_cc_myself">Cc myself:</label> <input type="checkbox" name="cc_myself" id="id_cc_myself"></p>'
    >>> print(f.as_p())
    <p><label for="id_subject">Subject:</label> <input id="id_subject" type="text" name="subject" maxlength="100" required></p>
    <p><label for="id_message">Message:</label> <input type="text" name="message" id="id_message" required></p>
    <p><label for="id_sender">Sender:</label> <input type="email" name="sender" id="id_sender" required></p>
    <p><label for="id_cc_myself">Cc myself:</label> <input type="checkbox" name="cc_myself" id="id_cc_myself"></p>

### f.as_ul()

as_ul() renders the form as a `<li>` tag, with each `<li>` tag containing one field. It does not include `<ul>` `</ul>` tags.

    >>> f = ContactForm()
    >>> f.as_ul()
    '<li><label for="id_subject">Subject:</label> <input id="id_subject" type="text" name="subject" maxlength="100" required></li>\n<li><label for="id_message">Message:</label> <input type="text" name="message" id="id_message" required></li>\n<li><label for="id_sender">Sender:</label> <input type="email" name="sender" id="id_sender" required></li>\n<li><label for="id_cc_myself">Cc myself:</label> <input type="checkbox" name="cc_myself" id="id_cc_myself"></li>'
    >>> print(f.as_ul())
    <li><label for="id_subject">Subject:</label> <input id="id_subject" type="text" name="subject" maxlength="100" required></li>
    <li><label for="id_message">Message:</label> <input type="text" name="message" id="id_message" required></li>
    <li><label for="id_sender">Sender:</label> <input type="email" name="sender" id="id_sender" required></li>
    <li><label for="id_cc_myself">Cc myself:</label> <input type="checkbox" name="cc_myself" id="id_cc_myself"></li>

### f.as_table()

Finally, as_table() outputs the form as an HTML `<table>`. This is exactly the same as print. In fact, when you print a form object, it calls its as_table() method behind the scenes:

    >>> f = ContactForm()
    >>> f.as_table()
    '<tr><th><label for="id_subject">Subject:</label></th><td><input id="id_subject" type="text" name="subject" maxlength="100" required></td></tr>\n<tr><th><label for="id_message">Message:</label></th><td><input type="text" name="message" id="id_message" required></td></tr>\n<tr><th><label for="id_sender">Sender:</label></th><td><input type="email" name="sender" id="id_sender" required></td></tr>\n<tr><th><label for="id_cc_myself">Cc myself:</label></th><td><input type="checkbox" name="cc_myself" id="id_cc_myself"></td></tr>'
    >>> print(f)
    <tr><th><label for="id_subject">Subject:</label></th><td><input id="id_subject" type="text" name="subject" maxlength="100" required></td></tr>
    <tr><th><label for="id_message">Message:</label></th><td><input type="text" name="message" id="id_message" required></td></tr>
    <tr><th><label for="id_sender">Sender:</label></th><td><input type="email" name="sender" id="id_sender" required></td></tr>
    <tr><th><label for="id_cc_myself">Cc myself:</label></th><td><input type="checkbox" name="cc_myself" id="id_cc_myself"></td></tr>

## Styling required or erroneous form rows

### Form.error_css_class & .required_css_class

Its pretty common to style form rows & fields that are required or have errors.

The Form class has couple of hooks you can use to add class attributes to required rows or to rows with errors: set the above class attributes.

    from django import forms

    class ContactForm(forms.Form):
        error_css_class = 'error'
        required_css_class = 'required'

        # ... and the rest of your fields here

Once you’ve done that, rows will be given "error" and/or "required" classes, as needed. The HTML will look something like:

    >>> f = ContactForm(data)
    >>> print(f.as_table())
    <tr class="required"><th><label class="required" for="id_subject">Subject:</label>    ...
    <tr class="required"><th><label class="required" for="id_message">Message:</label>    ...
    <tr class="required error"><th><label class="required" for="id_sender">Sender:</label>      ...
    <tr><th><label for="id_cc_myself">Cc myself:<label> ...
    >>> f['subject'].label_tag()
    <label class="required" for="id_subject">Subject:</label>
    >>> f['subject'].label_tag(attrs={'class': 'foo'})
    <label for="id_subject" class="foo required">Subject:</label>

## Config. Form elements' HTML id attributes and `<label>` tags

### Form.auto_id

By default form rendering method include the below:

- HTML id attributes on the form element.
- An HTML `<label>` tag designates which text is associated with which form element. This small enhancement makes forms more usable & more accessible to assitive devices.
- The id attribute values are generated by prepending id_ to the form field names.
- Use auto_id argument to the Form contructor to control id and label behavior. This argument must be bool or string.

If auto_id is False, then the output will not include `<label>` tags nor id attributes:

    >>> f = ContactForm(auto_id=False)
    >>> print(f.as_table())
    <tr><th>Subject:</th><td><input type="text" name="subject" maxlength="100" required></td></tr>
    <tr><th>Message:</th><td><input type="text" name="message" required></td></tr>
    <tr><th>Sender:</th><td><input type="email" name="sender" required></td></tr>
    <tr><th>Cc myself:</th><td><input type="checkbox" name="cc_myself"></td></tr>
    >>> print(f.as_ul())
    <li>Subject: <input type="text" name="subject" maxlength="100" required></li>
    <li>Message: <input type="text" name="message" required></li>
    <li>Sender: <input type="email" name="sender" required></li>
    <li>Cc myself: <input type="checkbox" name="cc_myself"></li>
    >>> print(f.as_p())
    <p>Subject: <input type="text" name="subject" maxlength="100" required></p>
    <p>Message: <input type="text" name="message" required></p>
    <p>Sender: <input type="email" name="sender" required></p>
    <p>Cc myself: <input type="checkbox" name="cc_myself"></p>

else if auto_id is True below is the result:

    >>> f = ContactForm(auto_id=True)
    >>> print(f.as_table())
    <tr><th><label for="subject">Subject:</label></th><td><input id="subject" type="text" name="subject" maxlength="100" required></td></tr>
    <tr><th><label for="message">Message:</label></th><td><input type="text" name="message" id="message" required></td></tr>
    <tr><th><label for="sender">Sender:</label></th><td><input type="email" name="sender" id="sender" required></td></tr>
    <tr><th><label for="cc_myself">Cc myself:</label></th><td><input type="checkbox" name="cc_myself" id="cc_myself"></td></tr>
    >>> print(f.as_ul())
    <li><label for="subject">Subject:</label> <input id="subject" type="text" name="subject" maxlength="100" required></li>
    <li><label for="message">Message:</label> <input type="text" name="message" id="message" required></li>
    <li><label for="sender">Sender:</label> <input type="email" name="sender" id="sender" required></li>
    <li><label for="cc_myself">Cc myself:</label> <input type="checkbox" name="cc_myself" id="cc_myself"></li>
    >>> print(f.as_p())
    <p><label for="subject">Subject:</label> <input id="subject" type="text" name="subject" maxlength="100" required></p>
    <p><label for="message">Message:</label> <input type="text" name="message" id="message" required></p>
    <p><label for="sender">Sender:</label> <input type="email" name="sender" id="sender" required></p>
    <p><label for="cc_myself">Cc myself:</label> <input type="checkbox" name="cc_myself" id="cc_myself"></p>

If on the other hand auto_id is set to string containg the format character '%s', then form output will include label & id.
For ex: , for a format string 'field_%s', a field named subject will get the id value 'field_subject'. Continuing our example:

    >>> f = ContactForm(auto_id='id_for_%s')
    >>> print(f.as_table())
    <tr><th><label for="id_for_subject">Subject:</label></th><td><input id="id_for_subject" type="text" name="subject" maxlength="100" required></td></tr>
    <tr><th><label for="id_for_message">Message:</label></th><td><input type="text" name="message" id="id_for_message" required></td></tr>
    <tr><th><label for="id_for_sender">Sender:</label></th><td><input type="email" name="sender" id="id_for_sender" required></td></tr>
    <tr><th><label for="id_for_cc_myself">Cc myself:</label></th><td><input type="checkbox" name="cc_myself" id="id_for_cc_myself"></td></tr>
    >>> print(f.as_ul())
    <li><label for="id_for_subject">Subject:</label> <input id="id_for_subject" type="text" name="subject" maxlength="100" required></li>
    <li><label for="id_for_message">Message:</label> <input type="text" name="message" id="id_for_message" required></li>
    <li><label for="id_for_sender">Sender:</label> <input type="email" name="sender" id="id_for_sender" required></li>
    <li><label for="id_for_cc_myself">Cc myself:</label> <input type="checkbox" name="cc_myself" id="id_for_cc_myself"></li>
    >>> print(f.as_p())
    <p><label for="id_for_subject">Subject:</label> <input id="id_for_subject" type="text" name="subject" maxlength="100" required></p>
    <p><label for="id_for_message">Message:</label> <input type="text" name="message" id="id_for_message" required></p>
    <p><label for="id_for_sender">Sender:</label> <input type="email" name="sender" id="id_for_sender" required></p>
    <p><label for="id_for_cc_myself">Cc myself:</label> <input type="checkbox" name="cc_myself" id="id_for_cc_myself"></p>

If auto_id is set to any other true value – such as a string that doesn’t include %s – then the library will act as if auto_id is True.

By default, auto_id is set to the string 'id_%s'.

### Form.label_suffix

A translateable string (default to a colon(:) in English) that will be appended after any label name when form is rendered. It is possible to omit it entirely or change the character.

    >>> f = ContactForm(auto_id='id_for_%s', label_suffix='')
    >>> print(f.as_ul())
    <li><label for="id_for_subject">Subject</label> <input id="id_for_subject" type="text" name="subject" maxlength="100" required></li>
    <li><label for="id_for_message">Message</label> <input type="text" name="message" id="id_for_message" required></li>
    <li><label for="id_for_sender">Sender</label> <input type="email" name="sender" id="id_for_sender" required></li>
    <li><label for="id_for_cc_myself">Cc myself</label> <input type="checkbox" name="cc_myself" id="id_for_cc_myself"></li>
    >>> f = ContactForm(auto_id='id_for_%s', label_suffix=' ->')
    >>> print(f.as_ul())
    <li><label for="id_for_subject">Subject -></label> <input id="id_for_subject" type="text" name="subject" maxlength="100" required></li>
    <li><label for="id_for_message">Message -></label> <input type="text" name="message" id="id_for_message" required></li>
    <li><label for="id_for_sender">Sender -></label> <input type="email" name="sender" id="id_for_sender" required></li>
    <li><label for="id_for_cc_myself">Cc myself -></label> <input type="checkbox" name="cc_myself" id="id_for_cc_myself"></li>

>*Note:* that the label suffix is added only if the last character of the label isn’t a punctuation character (in English, those are ., !, ? or :).

Fields an also defince their own label_suffix. This will take precedence over Form.label_suffix. The suffix can also be overriden at runtime using the label_suffix parameter to label_tag.

### Form.use_required_attribute

When set to True (the default), required form fields will have the required HTML attribute.

[Formsets](https://docs.djangoproject.com/en/3.2/topics/forms/formsets/) instantitate forms with use_required_attribute=False to avoid incorrect browser validation when addind and deleting forms from formsets.

## Configuring the rendering of a form's widget

### Form.default_render

Specifies the [renderer](https://docs.djangoproject.com/en/3.2/ref/forms/renderers/) to use for the form. Defaults to None which means to use the default renderer specified by the Form_Renderer settings.

You can set this as a class attribute when declaring your form or use the renderer argument to `Form.__init__().` For example:

    from django import forms

    class MyForm(forms.Form):
        default_renderer = MyRenderer()

    or

    form = MyForm(renderer=MyRenderer())
    # You need to define MyRenderer in settings

### Notes on field ordering

In the as_p(), as_ul() and as_table() shortcuts, the fields are displayed in the order in which you define them in your form class. For example, in the ContactForm example, the fields are defined in the order subject, message, sender, cc_myself. To reorder the HTML output, change the order in which those fields are listed in the class.

There are several other ways to customize the order:

- ### Form.field_order
  
  By default its set to None, which retains the order in which you define the fields in your form class. If it is ordered as a list of field names, the fields are ordered as specified by the list & remaining fields are set to default order. Unkown filed names in the list are ignored.

- ### Form.order_fields(filed_order)

You may rearrange the fields any time using order_fields() with a list of field names as in field_order.

### How Errors are Displayed

If you render a bound Form object, the act of renderind will automatically run the form's validation if it hasn't already happened. Output of errors is shown as list `<ul class="errorlist">`. This also depends on the output method you are using.

    >>> data = {'subject': '',
    ...         'message': 'Hi there',
    ...         'sender': 'invalid email address',
    ...         'cc_myself': True}
    >>> f = ContactForm(data, auto_id=False)
    >>> print(f.as_table())
    <tr><th>Subject:</th><td><ul class="errorlist"><li>This field is required.</li></ul><input type="text" name="subject" maxlength="100" required></td></tr>
    <tr><th>Message:</th><td><input type="text" name="message" value="Hi there" required></td></tr>
    <tr><th>Sender:</th><td><ul class="errorlist"><li>Enter a valid email address.</li></ul><input type="email" name="sender" value="invalid email address" required></td></tr>
    <tr><th>Cc myself:</th><td><input checked type="checkbox" name="cc_myself"></td></tr>
    >>> print(f.as_ul())
    <li><ul class="errorlist"><li>This field is required.</li></ul>Subject: <input type="text" name="subject" maxlength="100" required></li>
    <li>Message: <input type="text" name="message" value="Hi there" required></li>
    <li><ul class="errorlist"><li>Enter a valid email address.</li></ul>Sender: <input type="email" name="sender" value="invalid email address" required></li>
    <li>Cc myself: <input checked type="checkbox" name="cc_myself"></li>
    >>> print(f.as_p())
    <p><ul class="errorlist"><li>This field is required.</li></ul></p>
    <p>Subject: <input type="text" name="subject" maxlength="100" required></p>
    <p>Message: <input type="text" name="message" value="Hi there" required></p>
    <p><ul class="errorlist"><li>Enter a valid email address.</li></ul></p>
    <p>Sender: <input type="email" name="sender" value="invalid email address" required></p>
    <p>Cc myself: <input checked type="checkbox" name="cc_myself"></p>

### Customize Error List Format

By default, forms use django.form.utils.ErrorList to format validation errors. If you'd like to use an alternate class for displaying errors, you can pass that in construction time:

    >>> from django.forms.utils import ErrorList
    >>> class DivErrorList(ErrorList):
    ...     def __str__(self):
    ...         return self.as_divs()
    ...     def as_divs(self):
    ...         if not self: return ''
    ...         return '<div class="errorlist">%s</div>' % ''.join(['<div class="error">%s</div>' % e for e in self])
    >>> f = ContactForm(data, auto_id=False, error_class=DivErrorList)
    >>> f.as_p()
    <div class="errorlist"><div class="error">This field is required.</div></div>
    <p>Subject: <input type="text" name="subject" maxlength="100" required></p>
    <p>Message: <input type="text" name="message" value="Hi there" required></p>
    <div class="errorlist"><div class="error">Enter a valid email address.</div></div>
    <p>Sender: <input type="email" name="sender" value="invalid email address" required></p>
    <p>Cc myself: <input checked type="checkbox" name="cc_myself"></p>

### More Granular Output

The as_p(), as_ul(), and as_table() methods are shortcuts – they’re not the only way a form object can be displayed.

### *class* BoundField

- Used to display HTML or access attribute for a single field in Form instance.
- The `__str__` () method of this object displays the HTML for the field.

To retrieve a single BoundField, use dictionary lookup syntax on your form using the field’s name as the key:

    >>> form = ContactForm()
    >>> print(form['subject'])
    <input id="id_subject" type="text" name="subject" maxlength="100" required>

To retrieve all BoundField objects, iterate the form:

    >>> form = ContactForm()
    >>> for boundfield in form: print(boundfield)
    <input id="id_subject" type="text" name="subject" maxlength="100" required>
    <input type="text" name="message" id="id_message" required>
    <input type="email" name="sender" id="id_sender" required>
    <input type="checkbox" name="cc_myself" id="id_cc_myself">

The field-specific output honors the form object’s auto_id setting:

    >>> f = ContactForm(auto_id=False)
    >>> print(f['message'])
    <input type="text" name="message" required>
    >>> f = ContactForm(auto_id='id_%s')
    >>> print(f['message'])
    <input type="text" name="message" id="id_message" required>

## Attribute of BoundField

### BoundField.auto_id

The HTML ID attribute for this BoundField. Returns an empty string if Form.auto_id is False.

### BoundField.data

This property returns the data for this BoundField extracted by the widget’s value_from_datadict() method, or None if it wasn’t given:

    >>> unbound_form = ContactForm()
    >>> print(unbound_form['subject'].data)
    None
    >>> bound_form = ContactForm(data={'subject': 'My Subject'})
    >>> print(bound_form['subject'].data)
    My Subject

### BoundField.errors

A list-like object that is displayed as an HTML `<ul class="errorlist">` when printed:

    >>> data = {'subject': 'hi', 'message': '', 'sender': '', 'cc_myself': ''}
    >>> f = ContactForm(data, auto_id=False)
    >>> print(f['message'])
    <input type="text" name="message" required>
    >>> f['message'].errors
    ['This field is required.']
    >>> print(f['message'].errors)
    <ul class="errorlist"><li>This field is required.</li></ul>
    >>> f['subject'].errors
    []
    >>> print(f['subject'].errors)

    >>> str(f['subject'].errors)
    ''

- **BoundField.field** the form field instance from the form class that this BoundFiled wraps.
- **BoundField.form**: The Form instance this BoundFiled is bound to.
- **BoundField.help_text**: the help_text of the field
- **BoundField.html_name**: The name that will be used in the widgets HTML name attribute. It takes the form prefix into account.
- **BoundField.id_for_label**: Use this property to render the ID of this field. For Example, if you are manually constructing a `<label>` in your template (despite the fact that label_tags() will do this for you).

        <label for="{{ form.my_field.id_for_label }}">...</label>{{ my_field }}

  - By default, this will be the fields name prefix by id_("id_my_field" for the example above). You may modify the ID by setting attrs on the fields widget. For example declaring field like this.

        my_field = forms.CharField(widget=forms.TextInput(attrs={'id': 'myFIELD'}))

  - and using the template above, would render something like:

        <label for="myFIELD">...</label><input id="myFIELD" type="text" name="my_field" required>

- **BoundField.is_hidden**: Returns True if the BoundField's widget is hidden.
- **BoundField.label**: The label of the field. This is used in label_tag().
- **BoundField.name**: To display the name of the field in the form:

        >>> f = ContactForm()
        >>> print(f['subject'].name)
        subject
        >>> print(f['message'].name)
        message

- **BoundField.widget_type**: Its new in Django 3.1 version and later. Returns the lowercased class name of the wrapped field’s widget, with any trailing input or widget removed. This may be used when building forms where the layout is dependent upon the widget type. For example:

        {% for field in form %}
            {% if field.widget_type == 'checkbox' %}
                # render one way
            {% else %}
                # render another way
            {% endif %}
        {% endfor %}

### Methods of BoundField

- **BoundField.as_hidden(attrs=None, `**`kwargs)**: Returns a string of HTML for representing this is an `<input type="hidden">`. `**`kwargs are passed to as_widget(). This method is primarily used internally, you should use widget.
- **BoundField.as_widget(widget=None, attrs=None, only_initial=False)**: Renders the field by rendering the passed widget, adding any HTML attributes passed as attrs. If no widget is specified, then the field’s default widget will be used. only_initial is used by Django internals and should not be set explicitly.
- **BoundField.css_classes(extra_classes=None)**: When you use Django’s rendering shortcuts, CSS classes are used to indicate required form fields or fields that contain errors. If you’re manually rendering a form, you can access these CSS classes using the css_classes method:

        >>> f = ContactForm(data={'message': ''})
        >>> f['message'].css_classes()
        'required'

    if you want to provide some additional classes in addition to the error & requried classes that may be required, you can provide those classes as an argument.

        >>> f = ContactForm(data={'message': ''})
        >>> f['message'].css_classes('foo bar')
        'foo bar required'

- **BoundField.label_tag(contents=None, attrs=None, label_suffix=None)**: To separately render the label tag of a form field, you can call its label_tag() method:

        >>> f = ContactForm(data={'message': ''})
        >>> print(f['message'].label_tag())
        <label for="id_message">Message:</label>

    You can provide the contents parameter which will replace the auto-generated label tag. An attrs dict may contain additional attributes for the `<label>` tag.
    The HTML that’s generated includes the form’s label_suffix (a colon, by default) or, if set, the current field’s label_suffix. The optional label_suffix parameter allows you to override any previously set suffix. For example, you can use an empty string to hide the label on selected fields. If you need to do this in a template, you could write a custom filter to allow passing parameters to label_tag.
- **BoundField.value()**: Use this method to render the raw value of this field as it would be rendered by a Widget:

        >>> initial = {'subject': 'welcome'}
        >>> unbound_form = ContactForm(initial=initial)
        >>> bound_form = ContactForm(data={'subject': 'hi'}, initial=initial)
        >>> print(unbound_form['subject'].value())
        welcome
        >>> print(bound_form['subject'].value())
        hi

### Customizing BoundField

If you need to access some additional information about a form field in a template and using a subclass of Field isn’t sufficient, consider also customizing BoundField.

A custom form field can override get_bound_field():

- **Field.get_bound_field(form,field_name)**: Takes an instance of form & the name of the field. The return value will be used when accessing the field in a template. Most likely it will be an instance of a subclass of BoundField.

    If you have a GPSCoordinatesField, for example, and want to be able to access additional information about the coordinates in a template, this could be implemented as follows:

        class GPSCoordinatesBoundField(BoundField):
            @property
            def country(self):
                """
                Return the country the coordinates lie in or None if it can't be
                determined.
                """
                value = self.value()
                if value:
                    return get_country_from_coordinates(value)
                else:
                    return None

        class GPSCoordinatesField(Field):
            def get_bound_field(self, form, field_name):
                return GPSCoordinatesBoundField(form, self, field_name)

    Now you can access the country in a template with {{ form.coordinates.country }}.

### Binding upload files to a form

Dealing with filefield and imagefield is little more complicated than a normal form.

- To do so firstly, in order to upload files, need to make sure that `<form>` element correctly defines the enctype as "multipart/form-data":

        <form enctype="multipart/form-data" method="post" action="/foo/">

- next, when you use form, you need to bind the file data. File data is handeled seprately to normal form data, so when it contains a FileField/ImageField, you need to specify a second argument when you bind your form. So if we extend our ContactForm to include an ImageField called mugshot, we need to bind the file data containing the mugshot image:

        # Bound form with an image field
        >>> from django.core.files.uploadedfile import SimpleUploadedFile
        >>> data = {'subject': 'hello',
        ...         'message': 'Hi there',
        ...         'sender': 'foo@example.com',
        ...         'cc_myself': True}
        >>> file_data = {'mugshot': SimpleUploadedFile('face.jpg', <file data>)}
        >>> f = ContactFormWithMugshot(data, file_data)

In practice, you will usually specify request.FILES as the source of file data (just like you use request.POST as the source of form data):

    # Bound form with an image field, data from the request
    >>> f = ContactFormWithMugshot(request.POST, request.FILES)

Unbound form would look like this - omit both form & file data.

    # Unbound form with an image field
    >>> f = ContactFormWithMugshot()

### Testing for Multipart Forms

- **Form.is_multipart()**: Will return Bool value. Useful method when you're writing reusable views of templates, as you may not know ahead time that whether you will use multipart or not.

        >>> f = ContactFormWithMugshot()
        >>> f.is_multipart()
        True

    Here’s an example of how you might use this in a template:

        {% if form.is_multipart %}
            <form enctype="multipart/form-data" method="post" action="/foo/">
        {% else %}
            <form method="post" action="/foo/">
        {% endif %}
        {{ form }}
        </form>

- **Subclassing Forms**: In simple words you can subclass the exisiting form such as exisiting will act as parent and subclassed will act as a child. As per django if you have multiple forms which share fields you can use subclassing. When subclassing is done it include all the fields of the parent class, followed by any fields you define in the child class.

    Example as follows: ContactFormWithPriority copy all the fields of ContactForm includes additional filed of priority as mentioned by you.

        >>> class ContactFormWithPriority(ContactForm):
        ...     priority = forms.CharField()
        >>> f = ContactFormWithPriority(auto_id=False)
        >>> print(f.as_ul())
        <li>Subject: <input type="text" name="subject" maxlength="100" required></li>
        <li>Message: <input type="text" name="message" required></li>
        <li>Sender: <input type="email" name="sender" required></li>
        <li>Cc myself: <input type="checkbox" name="cc_myself"></li>
        <li>Priority: <input type="text" name="priority" required></li>

    You can also subclass form with 2 differ parents. As per django its possible to subclass multiple forms, treating forms in mixins. Example as follows:

        >>> from django import forms
        >>> class PersonForm(forms.Form):
        ...     first_name = forms.CharField()
        ...     last_name = forms.CharField()
        >>> class InstrumentForm(forms.Form):
        ...     instrument = forms.CharField()
        >>> class BeatleForm(InstrumentForm, PersonForm):
        ...     haircut_type = forms.CharField()
        >>> b = BeatleForm(auto_id=False)
        >>> print(b.as_ul())
        <li>First name: <input type="text" name="first_name" required></li>
        <li>Last name: <input type="text" name="last_name" required></li>
        <li>Instrument: <input type="text" name="instrument" required></li>
        <li>Haircut type: <input type="text" name="haircut_type" required></li>

    It's possible to declaratively remove a Field inherited from a parent class by setting the name of the field to None on the subclass. For example:

        >>> from django import forms

        >>> class ParentForm(forms.Form):
        ...     name = forms.CharField()
        ...     age = forms.IntegerField()

        >>> class ChildForm(ParentForm):
        ...     name = None

        >>> list(ChildForm().fields)
        ['age']

>*Note*: subclass can only do upto 2 classes as parents. This what I have tried in shell. May be it can do more but in django docs its not written

### Prefix for Forms

- **Form.prefix**: You can enter several Django Forms inside one `<form>` tag. To give each Form its namespace, use the prefix keyword argument.

        >>> mother = PersonForm(prefix="mother")
        >>> father = PersonForm(prefix="father")
        >>> print(mother.as_ul())
        <li><label for="id_mother-first_name">First name:</label> <input type="text" name="mother-first_name" id="id_mother-first_name" required></li>
        <li><label for="id_mother-last_name">Last name:</label> <input type="text" name="mother-last_name" id="id_mother-last_name" required></li>
        >>> print(father.as_ul())
        <li><label for="id_father-first_name">First name:</label> <input type="text" name="father-first_name" id="id_father-first_name" required></li>
        <li><label for="id_father-last_name">Last name:</label> <input type="text" name="father-last_name" id="id_father-last_name" required></li>

    The prefix can also be specified on the form class;

        >>> class PersonForm(forms.Form):
        ...     ...
        ...     prefix = 'person'

***

## Part II: Form Fields

### *class* Field(`**`*kwargs*)

When you create form the most import part is defining the field such as CharField, IntegerField etc.
Each field has custom validation logic, along with a few other hooks.

### Field.clean(value)

Each Field instance has clean() method, which takes a single argument & either raises a **django.core.exceptions.ValidationError** exception or returns the clean value:

    >>> from django import forms
    >>> f = forms.EmailField()
    >>> f.clean('foo@example.com')
    'foo@example.com'
    >>> f.clean('invalid email address')
    Traceback (most recent call last):
    ...
    ValidationError: ['Enter a valid email address.']

## Core Field Arguments

### Field.required

By default, each Field class assumes the value is required, so if you pass an empty value – either None or the empty string ("") – then clean() will raise a ValidationError exception:

    >>> from django import forms
    >>> f = forms.CharField()
    >>> f.clean('foo')
    'foo'
    >>> f.clean('')
    Traceback (most recent call last):
    ...
    ValidationError: ['This field is required.']
    >>> f.clean(None)
    Traceback (most recent call last):
    ...
    ValidationError: ['This field is required.']
    >>> f.clean(' ')
    ' '
    >>> f.clean(0)
    '0'
    >>> f.clean(True)
    'True'
    >>> f.clean(False)
    'False'

To specify that a field is not required, pass required=False to the Field constructor:

    >>> f = forms.CharField(required=False)
    >>> f.clean('foo')
    'foo'
    >>> f.clean('')
    ''
    >>> f.clean(None)
    ''
    >>> f.clean(0)
    '0'
    >>> f.clean(True)
    'True'
    >>> f.clean(False)
    'False'

If a Field has required=False and you pass clean() an empty value, then clean() will return a normalized empty value rather than raising ValidationError. For CharField, this will return empty_value which defaults to an empty string. For other Field classes, it might be None. (This varies from field to field.)

Widgets of required form fields have the required HTML attribute. Set the Form.use_required_attribute attribute to False to disable it. The required attribute isn’t included on forms of formsets because the browser validation may not be correct when adding and deleting formsets.

## LABEL

### Field.label

The label argument lets you specify the "human-friendly" label for this field. This is used when the Field is displayed in a Form.

Here’s a full example Form that implements label for two of its fields. We’ve specified auto_id=False to simplify the output:

    >>> from django import forms
    >>> class CommentForm(forms.Form):
    ...     name = forms.CharField(label='Your name')
    ...     url = forms.URLField(label='Your website', required=False)
    ...     comment = forms.CharField()
    >>> f = CommentForm(auto_id=False)
    >>> print(f)
    <tr><th>Your name:</th><td><input type="text" name="name" required></td></tr>
    <tr><th>Your website:</th><td><input type="url" name="url"></td></tr>
    <tr><th>Comment:</th><td><input type="text" name="comment" required></td></tr>

### Field.label_suffix

The label_suffix argument lets you override the form’s label_suffix on a per-field basis:

    >>> class ContactForm(forms.Form):
    ...     age = forms.IntegerField()
    ...     nationality = forms.CharField()
    ...     captcha_answer = forms.IntegerField(label='2 + 2', label_suffix=' =')
    >>> f = ContactForm(label_suffix='?')
    >>> print(f.as_p())
    <p><label for="id_age">Age?</label> <input id="id_age" name="age" type="number" required></p>
    <p><label for="id_nationality">Nationality?</label> <input id="id_nationality" name="nationality" type="text" required></p>
    <p><label for="id_captcha_answer">2 + 2 =</label> <input id="id_captcha_answer" name="captcha_answer" type="number" required></p>

### Field.initial

The initial argument lets you specify the initial value to use when rendering this Field in an unbound Form.

To specify dynamic initial data, see the [Form.initial](https://docs.djangoproject.com/en/3.2/ref/forms/api/#django.forms.Form.initial) parameter.

The use-case for this is when you want to display an “empty” form in which a field is initialized to a particular value. For example:

    >>> from django import forms
    >>> class CommentForm(forms.Form):
    ...     name = forms.CharField(initial='Your name')
    ...     url = forms.URLField(initial='http://')
    ...     comment = forms.CharField()
    >>> f = CommentForm(auto_id=False)
    >>> print(f)
    <tr><th>Name:</th><td><input type="text" name="name" value="Your name" required></td></tr>
    <tr><th>Url:</th><td><input type="url" name="url" value="http://" required></td></tr>
    <tr><th>Comment:</th><td><input type="text" name="comment" required></td></tr>

You may be thinking, why not just pass a dictionary of the initial values as data when displaying the form? Well, if you do that, you’ll trigger validation, and the HTML output will include any validation errors:

    >>> class CommentForm(forms.Form):
    ...     name = forms.CharField()
    ...     url = forms.URLField()
    ...     comment = forms.CharField()
    >>> default_data = {'name': 'Your name', 'url': 'http://'}
    >>> f = CommentForm(default_data, auto_id=False)
    >>> print(f)
    <tr><th>Name:</th><td><input type="text" name="name" value="Your name" required></td></tr>
    <tr><th>Url:</th><td><ul class="errorlist"><li>Enter a valid URL.</li></ul><input type="url" name="url" value="http://" required></td></tr>
    <tr><th>Comment:</th><td><ul class="errorlist"><li>This field is required.</li></ul><input type="text" name="comment" required></td></tr>

This is why initial values are only displayed for unbound forms. For bound forms, the HTML output will use the bound data.

Also note that initial values are not used as “fallback” data in validation if a particular field’s value is not given. initial values are only intended for initial form display:

    >>> class CommentForm(forms.Form):
    ...     name = forms.CharField(initial='Your name')
    ...     url = forms.URLField(initial='http://')
    ...     comment = forms.CharField()
    >>> data = {'name': '', 'url': '', 'comment': 'Foo'}
    >>> f = CommentForm(data)
    >>> f.is_valid()
    False
    # The form does *not* fall back to using the initial values.
    >>> f.errors
    {'url': ['This field is required.'], 'name': ['This field is required.']}

Instead of a constant, you can also pass any callable:

    >>> import datetime
    >>> class DateForm(forms.Form):
    ...     day = forms.DateField(initial=datetime.date.today)
    >>> print(DateForm())
    <tr><th>Day:</th><td><input type="text" name="day" value="12/23/2008" required><td></tr>

The callable will be evaluated only when the unbound form is displayed, not when it is defined.

### Field.widget

The widget argument lets you specify a Widget class to use when rendering this Field. See Widgets for more information. The widget handles the rendering of the HTML, and the extraction of data from a GET/POST dictionary that corresponds to the widget.

### Field.help_text

The help_text argument lets you specify descriptive text for this Field. If you provide help_text, it will be displayed next to the Field when the Field is rendered by one of the convenience Form methods (e.g., as_ul()).

    >>> from django import forms
    >>> class HelpTextContactForm(forms.Form):
    ...     subject = forms.CharField(max_length=100, help_text='100 characters max.')
    ...     message = forms.CharField()
    ...     sender = forms.EmailField(help_text='A valid email address, please.')
    ...     cc_myself = forms.BooleanField(required=False)
    >>> f = HelpTextContactForm(auto_id=False)
    >>> print(f.as_table())
    <tr><th>Subject:</th><td><input type="text" name="subject" maxlength="100" required><br><span class="helptext">100 characters max.</span></td></tr>
    <tr><th>Message:</th><td><input type="text" name="message" required></td></tr>
    <tr><th>Sender:</th><td><input type="email" name="sender" required><br>A valid email address, please.</td></tr>
    <tr><th>Cc myself:</th><td><input type="checkbox" name="cc_myself"></td></tr>
    >>> print(f.as_ul()))
    <li>Subject: <input type="text" name="subject" maxlength="100" required> <span class="helptext">100 characters max.</span></li>
    <li>Message: <input type="text" name="message" required></li>
    <li>Sender: <input type="email" name="sender" required> A valid email address, please.</li>
    <li>Cc myself: <input type="checkbox" name="cc_myself"></li>
    >>> print(f.as_p())
    <p>Subject: <input type="text" name="subject" maxlength="100" required> <span class="helptext">100 characters max.</span></p>
    <p>Message: <input type="text" name="message" required></p>
    <p>Sender: <input type="email" name="sender" required> A valid email address, please.</p>
    <p>Cc myself: <input type="checkbox" name="cc_myself"></p>

### Field.error_messages

The error_messages argument lets you override the default messages that the field will raise. Pass in a dictionary with keys matching the error messages you want to override. For example, here is the default error message:

    >>> from django import forms
    >>> generic = forms.CharField()
    >>> generic.clean('')
    Traceback (most recent call last):
    ...
    ValidationError: ['This field is required.']

And here is a custom error message:

    >>> name = forms.CharField(error_messages={'required': 'Please enter your name'})
    >>> name.clean('')
    Traceback (most recent call last):
    ...
    ValidationError: ['Please enter your name']

In the built-in Field classes section below, each Field defines the error message keys it uses.

### Field.validators

The validators argument lets you provide a list of validation functions for this field.
See the [validators documents](https://docs.djangoproject.com/en/3.2/ref/validators/).

### Field.localize

The [localize](https://docs.djangoproject.com/en/3.2/topics/i18n/formatting/) argument enables the localization of form data input, as well as the rendered output.

Django’s formatting system is capable of displaying dates, times and numbers in templates using the format specified for the current locale. It also handles localized input in forms.

When it’s enabled, two users accessing the same content may see dates, times and numbers formatted in different ways, depending on the formats for their current locale.

The formatting system is disabled by default. To enable it, it’s necessary to set USE_L10N = True in your settings file.

### Field.disabled

The disabled boolean argument, when set to True, disables a form field using the disabled HTML attribute so that it won’t be editable by users. Even if a user tampers with the field’s value submitted to the server, it will be ignored in favor of the value from the form’s initial data.

### Field.has_changed()

The has_changed() method is used to determine if the field value has changed from the initial value. Returns True or False.

## Built-in Field Classes

Naturally, the forms library comes with a set of Field classes that represent common validation needs. This section documents each built-in field.

For each field, we describe the default widget used if you don’t specify widget. We also specify the value returned when you provide an empty value (see the section on required above to understand what that means).

### BooleanField class (`**`*kwargs*)

- Default widget: CheckboxInput
- Empty Value: False
- Normalize to: A Python True or False value
- Validates that the value is True(e.g. the check box is checked) if the field has required=True
- Error message keys: required

>*Note*: Since all Field subclasses have required=True by default, the validation condition here is important. If you want to include a boolean in your form that can be either True or False (e.g. a checked or unchecked checkbox), you must remember to pass in required=False when creating the BooleanField.

### CharField

- Default widget: TextInput
- Empty value: Whatever is given as empty_value
- Normalizes: Represent a string
- Uses MaxlengthValidator and MinLengthValidator if max_length and min_length are provided. Otherwise, all inputs are valid.
- Error message keys: required, max_length, min_length

    Has four optional arguments for validation:

  - max_length
  - min_length: If provided, these arguments ensure that the string is at most or at least the given length.
  - strip: If True (default), the value will be stripped of leading and trailing whitespace.
  - empty_value: The value to use to represent “empty”. Defaults to an empty string.

### ChoiceField

- Default widget: Select
- Empty value: '' An empty string
- Normalizes: To Represent a string
- Validates that the given value exits in the list of choices.
- Error message keys: required, invalid_choice

The invalid_choice error message may contain %(value)s, which will be replaced with the selected choice.

### TypeChoiceField

Just like a ChoiceField, except TypedChoiceField takes two extra arguments, coerce and empty_value.

- Default widget: Select
- Empty value: Whatever is given as empty_value.
- Normalizes to: A value of the type provided by the coerce argument.
- alidates that the given value exists in the list of choices and can be coerced.
- Error message keys: required, invalid_choice

**coerce**: A function that takes one argument and returns a coerced value. Examples include the built-in int, float, bool and other types. Defaults to an identity function. Note that coercion happens after input validation, so it is possible to coerce to a value not present in choices

**empty_value**: The value to use to represent “empty.” Defaults to the empty string; None is another common choice here. Note that this value will not be coerced by the function given in the coerce argument, so choose it accordingly.

### DateField, DateTimeField(`**`*kwargs*)

- Default: DateInput
- Empty value: None
- Normalizes: to represent a python datetime.date object
- Validates that it is a datetime.date.datetime.datetime or string formatted in a particular date format.
- Error: required, invalid

**input_formats**: A list of formats used to attempt to convert a string to a valid datetime.datetime object, in addition to ISO 8601 formats.

The field always accepts strings in ISO 8601 formatted dates or similar recognized by parse_datetime(). Some examples are:

    * '2006-10-25 14:30:59'
    * '2006-10-25T14:30:59'
    * '2006-10-25 14:30'
    * '2006-10-25T14:30'
    * '2006-10-25T14:30Z'
    * '2006-10-25T14:30+02:00'
    * '2006-10-25'

>**Changed in Django 3.1:**
Support for ISO 8601 date string parsing (including optional timezone) was added.
The fallback on DATE_INPUT_FORMATS in the default input_formats was added.

### DecimalField(`**`*kwargs*)

- Default: NumberInput when Field.localize is False, else TextInput
- Empty Value: None
- Normalizes: To represent a Python decimal
- Validates: That value is a decimal. Uses MaxValueValidator and MinValueValidator if max_value and min_value are provided. Leading and trailing whitespace is ignored.
- Error Messages: required, invalid, max_value, min_value, max_digits, max_decimal_places, max_whole_digits

The max_value and min_value error messages may contain %(limit_value)s, which will be substituted by the appropriate limit. Similarly, the max_digits, max_decimal_places and max_whole_digits error messages may contain %(max)s.

Takes four optional arguments:

**max_value** or **min_value**:
These control the range of values permitted in the field, and should be given as decimal.Decimal values.

**max_digits:**
The maximum number of digits (those before the decimal point plus those after the decimal point, with leading zeros stripped) permitted in the value.

**decimal_places:**
The maximum number of decimal places permitted.

### DurationField(`**`*kwargs*)

- Default: TextInput
- Empty value: None
- Represents as Python timedelta.
- Validates: A string which can be converted to timedelta.
- Error messages: required, invalid, overflow

### EmailField(`**`*kwargs*)

- Default: EmailInput
- Empty Value: whatever given as empty_value
- Represents a Python string
- Validation: EmailValidator applied to check if it is a emailfield
- Error message: required, invalid

### FileField(`**`*kwargs*)

- Default: ClearableFileField
- Empty Value: None
- Represents: An uploaded file object that wraps the file content & file name into a single object.
- Validates: That non-empty file data has been bound to the form.
- Error Messages: required, invalid, missing, empty, max_length

### FilePathField(`**`*kwargs*)

- Default: Select
- Empty: '' (empty string)
- Represents to a sring
- Validates: choice exits in the list
- Error Messages: required, invalid_choice

**Path**: The absolute path to the directory whose contents you want listed. This directory must exits.

**allow_files or allow_folder**: Either True or False in both args. Default True, later Default False: Specifies the files in the specified location should be included.

### FloatField(`**`*kwargs*)

- Default: NumberInput when Field.localize is False, else TextInput
- Empty value: None
- Represents a Python float
- Validates: that the given value is float. Uses Max-MinValueValidator if max_value or min_value is provided.
- Error message keys: required, invalid, max_value, min_value

### ImageField(`**`*kwargs*)

- Default: ClearableFileInput
- Empty Value: None
- Normalizes to: An UploadedFile object that wraps the file content and file name into a single object.
- Validates: That file is bound to the form. Also uses FileExtensionValidator to validate that the file extension is supported by Pillow.
- Error message keys: required, invalid, missing, empty, invalid_image

Using an ImageField requires that [Pillow](https://pillow.readthedocs.io/en/latest/) is installed with support for the image formats you use. If you encounter a corrupt image error when you upload an image, it usually means that Pillow doesn’t understand its format. To fix this, install the appropriate library and reinstall Pillow.

When you use an ImageField on a form, you must also remember to bind the file data to the form.

After the field has been cleaned and validated, the UploadedFile object will have an additional image attribute containing the Pillow Image instance used to check if the file was a valid image. Pillow closes the underlying file descriptor after verifying an image, so while non-image data attributes, such as format, height, and width, are available, methods that access the underlying image data, such as getdata() or getpixel(), cannot be used without reopening the file. For example:

    >>> from PIL import Image
    >>> from django import forms
    >>> from django.core.files.uploadedfile import SimpleUploadedFile
    >>> class ImageForm(forms.Form):
    ...     img = forms.ImageField()
    >>> file_data = {'img': SimpleUploadedFile('test.png', <file data>)}
    >>> form = ImageForm({}, file_data)
    # Pillow closes the underlying file descriptor.
    >>> form.is_valid()
    True
    >>> image_field = form.cleaned_data['img']
    >>> image_field.image
    <PIL.PngImagePlugin.PngImageFile image mode=RGBA size=191x287 at 0x7F5985045C18>
    >>> image_field.image.width
    191
    >>> image_field.image.height
    287
    >>> image_field.image.format
    'PNG'
    >>> image_field.image.getdata()
    # Raises AttributeError: 'NoneType' object has no attribute 'seek'.
    >>> image = Image.open(image_field)
    >>> image.getdata()
    <ImagingCore object at 0x7f5984f874b0>

Code as found on Stack Overflow

    from PIL import Image
    from django import forms
    from django.core.files.uploadedfile import SimpleUploadedFile
    class ImageForm(forms.Form):
        img = forms.ImageField()

    img_data = None
    with open('test.png', 'rb') as img_file:
        img_data = img_file.read()

    file_data = {'img': SimpleUploadedFile('test.png', img_data)}
    >>> f.is_valid()
    True
    >>> image_field = f.cleaned_data['img']
    >>> image_field.image
    <PIL.PngImagePlugin.PngImageFile image mode=RGBA size=1444x1004 at 0x7FD738138D30>
    >>> image_field.image.width
    1444
    >>> image_field.image.height
    1004
    >>> image_field.image.format
    'PNG'
    >>> image_field.image.getdata()
    Traceback (most recent call last): seek
    >>> image = Image.open(image_field)
    >>> image.getdata()
    <ImagingCore object at 0x7fd7380f8d10>

### IntegerField

- Default: NumberInput
- Empty Value: None
- Represents a Python integer
- Validates: That the given value is integer. Leading and trailing whitespace is allowed, as in Python’s int() function.
- Error Message Keys: required, invalid, max_value, min_value

### JSONField(encoder=None, decoder=None, `**`kwargs)

> New in Django 3.1

- Default: Textarea
- Empty value: None
- Normalizes to: A Python representation of the JSON value (usually as a dict, list, or None), depending on JSONField.decoder
- Validates: That its a valid JSON
- Error message keys: required, invalid

Takes two optional arguments:

**encoder**: A [json.JSONEncoder](https://docs.python.org/3/library/json.html#json.JSONEncoder) subclass to serialize data types not supported by the standard JSON serializer (e.g. datetime.datetime or UUID). For example, you can use the DjangoJSONEncoder class.

**decoder**: A [json.JSONDecoder](https://docs.python.org/3/library/json.html#json.JSONDecoder) subclass to deserialize the input. Your deserialization may need to account for the fact that you can’t be certain of the input type. For example, you run the risk of returning a datetime that was actually a string that just happened to be in the same format chosen for datetimes.

The decoder can be used to validate the input. If json.JSONDecodeError is raised during the deserialization, a ValidationError will be raised.

Defaults to json.JSONDecoder.

>*Note:*
If you use a ModelForm, the encoder and decoder from JSONField will be used.
>*User friendly forms:*
JSONField is not particularly user friendly in most cases. However, it is a useful way to format data from a client-side widget for submission to the server.

### GenericIPAddressField

A field containing either an IPv4 or an IPv6 address.

- Default: TextInput
- Empty Value: '' (an empty string)
- Normalizes to: A string. IPv6 addresses are normalized as described below
- Validation: check the given value is valid IP address
- Error message keys: required, invalid

The IPv6 address normalization follows RFC 4291#section-2.2 section 2.2, including using the IPv4 format suggested in paragraph 3 of that section, like ::ffff:192.0.2.0. For example, 2001:0::0:01 would be normalized to 2001::1, and ::ffff:0a0a:0a0a to ::ffff:10.10.10.10. All characters are converted to lowercase.

Takes two optional arguments:

**protocol**:
Limits valid inputs to the specified protocol. Accepted values are both (default), IPv4 or IPv6. Matching is case insensitive.

**unpack_ipv4**:
Unpacks IPv4 mapped addresses like ::ffff:192.0.2.1. If this option is enabled that address would be unpacked to 192.0.2.1. Default is disabled. Can only be used when protocol is set to 'both'.

### MultipleChoiceField

- Default: SelectMultiple
- Empty Value: [] (an empty list)
- Normalizes: A list of strings
- Validates: that list of values exists in the list of choices
- Error Message key: required, invalid_choice, invalid_list

The invalid_choice error message may contain %(value)s, which will be replaced with the selected choice.
Takes one extra required argument, choices, as for ChoiceField.

### TypedMultipleChoiceField

Just like a MultipleChoiceField, except TypedMultipleChoiceField takes two extra arguments, coerce and empty_value.

- Default: SelectMultiple
- Empty Value: Whatever you're given as empty
- Normalizes: A list of value of the type provided by coerce argument.
- Validates: that given values exists in the list of choices & can be coerced.
- Error Message key: required, invalid_choice

The invalid_choice error message may contain %(value)s, which will be replaced with the selected choice.
Takes two extra arguments, coerce and empty_value, as for TypedChoiceField.

### NullBooleanField

- Default: NullBooleanSelect
- Empty Value: None
- Normalizes: A Python True, False or None
- Validates: nothing (never raises a ValidationError)

NullBooleanField may be used with widgets such as Select or RadioSelect by providing widget choices:

    NullBooleanField(
        widget=Select(
            choices=[
                ('', 'Unknown'),
                (True, 'Yes'),
                (False, 'No'),
            ]
        )
    )

### RegexField

- Default: TextInput
- Empty Value: whatever you leave as empty
- Normalizes to: A string
- Validates: Uses RegexValidator to validate that the given value matches a certain regular expression.
- Error messages key: required, invalid

Takes one required argument:

**regex**:
A regular expression specified either as a string or a compiled regular expression object.

Also takes max_length, min_length, strip, and empty_value which work just as they do for CharField.

**strip**:
Defaults to False. If enabled, stripping will be applied before the regex validation.

### SlugField

- Default: TextInput
- Empty Value: whatever is left as empty by you
- Normalizes to: A string
- Validates: Uses validate_slug or validate_unicode_slug that given value contains only letters, numbers, underscores & hyphens.
- Error message keys: required, invalid

This field is intended for use in representing a model SlugField in forms.

Takes two optional parameters:

**allow_unicode**:
A boolean instructing the field to accept Unicode letters in addition to ASCII letters. Defaults to False.

**empty_value**:
The value to use to represent “empty”. Defaults to an empty string.

### TimeField

- Default: TimeInput
- Empty Value: None
- Normalizes to: A Python datetime.time object
- Validates: that the given value is either a datetime.time or string formatted in a particular time format.
- Error message keys: required, invalid

Takes one optional argument:

**input_formats**:
A list of formats used to attempt to convert a string to a valid datetime.time object.

If no input_formats argument is provided, the default input formats are taken from TIME_INPUT_FORMATS if USE_L10N is False, or from the active locale format TIME_INPUT_FORMATS key if localization is enabled. See also format localization.

### URLField

- Default: URLInput
- Empty Value: whatever is left by you as empty
- Normalizes to: A string
- Validates: Uses URLValidators to validate that the given value is valid URL.
- Error message keys: required, invalid

Has three optional arguments max_length, min_length, and empty_value which work just as they do for CharField.

### UUIDField

- Default: TextInput
- Empty: None
- Normalizes to: A UUID object
- Error message keys: required, invalid

This field will accept any string format accepted as the hex argument to the UUID constructor.

## SLIGHTLY COMPLEX BUILT-IN FIELD CLASSES

### ComboField

- Default: TextInput
- Empty Values: '' (an empty string)
- Normalizes to: A string
- Validates: that given value against each of the fields specified as an argument to the ComboField
- Error message keys: required, invalid

Takes one extra required argument:

**fields:**
The list of fields that should be used to validate the field’s value (in the order in which they are provided).

    >>> from django.forms import ComboField
    >>> f = ComboField(fields=[CharField(max_length=20), EmailField()])
    >>> f.clean('test@example.com')
    'test@example.com'
    >>> f.clean('longemailaddress@example.com')
    Traceback (most recent call last):
    ...
    ValidationError: ['Ensure this value has at most 20 characters (it has 28).']

### MutiValueField

- Default: TextInput
- Empty value: '' (an empty string)
- Normalizes to: the type returned by the compress method of the subclass.
- Validates: the given value against each of the fields specified as an argument to MultiValueField
- Error message keys: required, invalid, incomplete

Aggregates the logic of multiple fields that together produce a single value.

This field is abstract and must be subclassed. In contrast with the single-value fields, subclasses of MultiValueField must not implement clean() but instead - implement compress().

Takes one extra required argument:

**fields:**
A tuple of fields whose values are cleaned and subsequently combined into a single value. Each value of the field is cleaned by the corresponding field in fields – the first value is cleaned by the first field, the second value is cleaned by the second field, etc. Once all fields are cleaned, the list of clean values is combined into a single value by compress().

Also takes some optional arguments:

**require_all_fields:**
Defaults to True, in which case a required validation error will be raised if no value is supplied for any field.

When set to False, the Field.required attribute can be set to False for individual fields to make them optional. If no value is supplied for a required field, an incomplete validation error will be raised.

A default incomplete error message can be defined on the MultiValueField subclass, or different messages can be defined on each individual field. For example:

    from django.core.validators import RegexValidator

    class PhoneField(MultiValueField):
        def __init__(self, **kwargs):
            # Define one message for all fields.
            error_messages = {
                'incomplete': 'Enter a country calling code and a phone number.',
            }
            # Or define a different message for each field.
            fields = (
                CharField(
                    error_messages={'incomplete': 'Enter a country calling code.'},
                    validators=[
                        RegexValidator(r'^[0-9]+$', 'Enter a valid country calling code.'),
                    ],
                ),
                CharField(
                    error_messages={'incomplete': 'Enter a phone number.'},
                    validators=[RegexValidator(r'^[0-9]+$', 'Enter a valid phone number.')],
                ),
                CharField(
                    validators=[RegexValidator(r'^[0-9]+$', 'Enter a valid extension.')],
                    required=False,
                ),
            )
            super().__init__(
                error_messages=error_messages, fields=fields,
                require_all_fields=False, **kwargs
            )

**widget:**
Must be a subclass of django.forms.MultiWidget. Default value is TextInput, which probably is not very useful in this case.

**compress(data_list):**
Takes a list of valid values and returns a “compressed” version of those values – in a single value. For example, SplitDateTimeField is a subclass which combines a time field and a date field into a datetime object.

This method must be implemented in the subclasses.

### SplitDateTimeField

- Default: [SplitDateTimeWidget](https://docs.djangoproject.com/en/3.2/ref/forms/widgets/#django.forms.SplitDateTimeWidget)
- Empty Value: None
- Normalize to: A Python datetime.datetime object
- Validates: that given value is datetime.datetime or string in the format of datetime.
- Error message keys: required, invalid, invalid_date, invalid_time

Takes two optional arguments:

**input_date_formats:**

- A list of formats used to attempt to convert a string to a valid datetime.date object.
- If no input_date_formats argument is provided, the default input formats for DateField are used.

**input_time_formats:**

- A list of formats used to attempt to convert a string to a valid datetime.time object.
- If no input_time_formats argument is provided, the default input formats for TimeField are used.

***

## Model Form Functions

### model_form factory

(model, form=ModelForm, fields=None, exclude=None, formfield_callback=None, widgets=None, localized_fields=None, labels=None, help_texts=None, error_messages=None, field_classes=None)

- Returns a ModelForm class for the given model. You can optionally pass a form argument to use as a starting point for constructing the ModelForm.
- Fields: is an optional list of fields name. If provided, only the names field will be included in the returned fields.
- excludes: is an optional list of fields name. If provided, the names field will be excluded from the return fields, even if they are listed in the fields arguments.
- formfield_callback: is a callable that takes models field & returns a form field.
- widgets: is a dict of model field names mapped to widget.
- localized_fields: is a list of fields which should be localized.
- labels: is a dicst of model field names mapped to labels.
- help_texts: is a dict of model field names mapped to a help_texts.
- error_messages: mapped to dict of error messages.
- field_classes: mapped to form field class

See the [modelform factory function](https://docs.djangoproject.com/en/3.2/topics/forms/modelforms/#modelforms-factory) to understand with example.

### modelformset_factory

(model, form=ModelForm, formfield_callback=None, formset=BaseModelFormSet, extra=1, can_delete=False, can_order=False, max_num=None, fields=None, exclude=None, widgets=None, validate_max=False, localized_fields=None, labels=None, help_texts=None, error_messages=None, min_num=None, validate_min=False, field_classes=None, absolute_max=None, can_delete_extra=True)

- Returns: a formset class for the given model class.
- Arguments model:, form, fields, exclude, formfield_callback, widgets, localized_fields, labels, help_texts, error_messages, and field_classes are all passed through to modelform_factory().
- Arguments formset:extra, can_delete, can_order, max_num, validate_max, min_num, validate_min, absolute_max, and can_delete_extra are passed through to formset_factory(). see [formsets](https://docs.djangoproject.com/en/3.2/topics/forms/formsets/) for more details.

### inlineformset_factory

(parent_model, model, form=ModelForm, formset=BaseInlineFormSet, fk_name=None, fields=None, exclude=None, extra=3, can_order=False, can_delete=True, max_num=None, formfield_callback=None, widgets=None, validate_max=False, localized_fields=None, labels=None, help_texts=None, error_messages=None, min_num=None, validate_min=False, field_classes=None, absolute_max=None, can_delete_extra=True)

Returns an InlineFormSet using modelformset_factory() with defaults of formset=BaseInlineFormSet, can_delete=True, and extra=3.

If your model has more than one ForeignKey to the parent_model, you must specify a fk_name.

***

## The Form Rendering API

Djangos form widgets are rendered using Django's [template engines system](https://docs.djangoproject.com/en/3.2/topics/templates/).
The form rendering process can be customized at several levels:

- Widgets can specify custom template names.
- Forms & widgets can specify custome renderer classes.
- A widget template can be overridden by project. (Reusable applications typically shouldn’t override built-in templates because they might conflict with a project’s custom templates.)

### The Low-Level Render API

- The rendering of form templates is controlled by customisable renderer class. 
- Custom renderer can be specified by updating the [Form_Renderer](https://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-FORM_RENDERER) settings.
- It defaults to 'django.forms.renderers.DjangoTemplates'.

You can also provide a custom renderer by setting the Form.default_renderer attribute or by using the renderer argument of Widget.render().

Use one of the built-in template form renderers or implement your own. Custom renderers must implement a render(template_name, context, request=None) method. It should return a rendered templates (as a string) or raise TemplateDoesNotExist.

### Built-in Template from renderers

**class DjangoTemplates**:

- This renderer uses a standalone DjangoTemplates engine(unconnected to what you might have configured in the TEMPLATES setting).
- Loads templates first from the built-in form templates dir in django/forms/templates.
- And than from the installed apps, templates dir using the app_directories loader.

If you want to render templates with customizations from your TEMPLATES setting, such as context processors for example, use the TemplatesSetting renderer.

**class Jinja2**:

- same as DjangoTemplates, except that it uses Jinja2 backend.
- located in the django/forms/jinja2
- installed apps can provide templates in jinja2 dir.
- To use this backend, all widgets & third parties must have Jinja2 templates.
- Unless you provide your own Jinja2 templates for widgets that don’t have any, you can’t use this renderer.
  - For example, django.contrib.admin doesn’t include Jinja2 templates for its widgets due to their usage of Django template tags.

**class TemplateSetting**:

- The renderer gives you control of how widget templates are sourced.
- It uses get_template() to find the widget templates based on what's configuired in the Templates setting.
- Using this renderer along with the built-in widget templates requires either:
  - 'django.forms' in INSTALLED_APPS and at least one engine with APP_DIRS=True.
  - Adding the built-in widgets templates directory in DIRS of one of your template engines. To generate that path:
 
            import django
            django.__path__[0] + '/forms/templates'  # or '/forms/jinja2'
