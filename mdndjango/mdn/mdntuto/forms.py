from django import forms


class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)
    user_name = forms.CharField(label='Last name', max_length=20, required=True)
    mobile_number = forms.IntegerField(label='Contact No.')
    email = forms.EmailField(label='Email Address', initial='foo@foo.com', required=True)
    date_of_birth = forms.DateField(label='Enter DOB', initial='YYYY-MM-DD format')

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)

class AuthorForm(forms.Form):
    name = forms.CharField(max_length=100)
    title = forms.CharField(
        max_length=3
    )
    birth_date = forms.DateField(required=False)


class AricleForm(forms.Form):
    title = forms.CharField(max_length=100)
    pub_date = forms.DateField()