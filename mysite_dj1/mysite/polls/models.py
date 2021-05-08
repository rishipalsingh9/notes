import datetime

from django.db import models
from django.utils import timezone

# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=208)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text
    
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Choice(models.Model):
    id = models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=208)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


# 1 published_recently logic
"""def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)"""
