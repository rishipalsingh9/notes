from django.core import validators
from django import forms
from .models import *  

class AddAgent(forms.ModelForm):
    class Meta:
        model = Agent
        fields = '__all__'