import datetime

from django.db import models
from django.utils import timezone

# Create your models here.

class Question(models.Model):
    id = models.BigAutoField(primary_key=True)
    question_text = models.CharField(max_length=208)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text
    
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE, primary_key=True)
    choice_text = models.CharField(max_length=208)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text