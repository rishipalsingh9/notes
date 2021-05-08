from django.contrib import admin

from polls.models import *

# Register your models here.

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inline = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
