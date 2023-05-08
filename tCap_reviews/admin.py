from django.contrib import admin
from .models import Nationality, Author, Category, Opus, Review, Comment, OpusList, UserRating
from django import forms
from django.forms import TextInput, Textarea
from django.db import models

#admin.site.register(Nationality)
#admin.site.register(Author)
#admin.site.register(Category)
#admin.site.register(Opus)
#admin.site.register(Review)
#admin.site.register(Comment)
#admin.site.register(OpusList)
#admin.site.register(UserRating)

class ModelWithExpandableCharFieldAndSearchableName(admin.ModelAdmin):

    search_fields = ['name']

    formfield_overrides = {
        #models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        #models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':160})},
        models.CharField: {'widget': Textarea(attrs={'rows':2, 'cols':20})},
    }

class ModelWithSearchableName(admin.ModelAdmin):

    search_fields = ['name']

admin.site.register(Author, ModelWithExpandableCharFieldAndSearchableName)
admin.site.register(Opus, ModelWithExpandableCharFieldAndSearchableName)

admin.site.register(Nationality, ModelWithSearchableName)
admin.site.register(Category, ModelWithSearchableName)
