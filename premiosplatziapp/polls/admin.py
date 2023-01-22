from django.contrib import admin
from .models import Question, Choice
from django import forms
from django.forms.models import BaseInlineFormSet


class ChoiceInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        # Check that no two choices have the same text
        texts = []
        for form in self.forms:
            text = form.cleaned_data.get('choice_text')
            if text in texts:
                raise forms.ValidationError('Choices must have unique texts.')
            texts.append(text)
        

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2
    formset = ChoiceInlineFormSet


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']

# Register your models here.
admin.site.register(Question, QuestionAdmin)

