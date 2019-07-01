from django.contrib import admin
from .models import *


class PublisherAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


admin.site.register(Publisher, PublisherAdmin)


class CreatorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'type']


admin.site.register(Creator, CreatorAdmin)


class SubjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


admin.site.register(Subject, SubjectAdmin)


class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'publisher', 'creator_string', 'price', 'isbn']
    list_filter = ['title', 'publisher']


admin.site.register(Book, BookAdmin)

