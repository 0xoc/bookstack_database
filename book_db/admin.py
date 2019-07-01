from django.contrib import admin
from .models import *


class PublisherAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['id', 'name']


admin.site.register(Publisher, PublisherAdmin)


class CreatorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'type']
    search_fields = ['id', 'name']


admin.site.register(Creator, CreatorAdmin)


class SubjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['id', 'name']


admin.site.register(Subject, SubjectAdmin)


class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'publisher', 'creator_string', 'price', 'isbn']
    search_fields = ['isbn', 'title', 'publisher__name', 'creators__name']


admin.site.register(Book, BookAdmin)

