from django.db import models
from django import forms

# Create your models here.
from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm, Textarea

TITLE_CHOICES = [
    ('MR', 'Mr.'),
    ('MRS', 'Mrs.'),
    ('MS', 'Ms.'),
]


class Author(models.Model):
    name = models.CharField(max_length=10)
    title = models.CharField(max_length=3, choices=TITLE_CHOICES)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)


#class AuthorForm(ModelForm):
#    class Meta:
#        model = Author
#        fields = ['name', 'title', 'birth_date']
#        widgets = {
#            'name': Textarea(attrs={'cols': 80, 'rows': 20}),
#        }

class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ('name', 'title', 'birth_date')
        labels = {
            'name': _('Writer'),
        }
        help_texts = {
            'name': _('Some useful help text.'),
        }
        error_messages = {
            'name': {
                'max_length': _("This writer's name is too long."),
            },
        }


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'authors']


class AuthorForm(forms.Form):
    name = forms.CharField(max_length=100)
    title = forms.CharField(
        max_length=3,
        widget=forms.Select(choices=TITLE_CHOICES),
    )
    birth_date = forms.DateField(required=False)


class BookForm(forms.Form):
    name = forms.CharField(max_length=100)
    authors = forms.ModelMultipleChoiceField(queryset=Author.objects.all())
