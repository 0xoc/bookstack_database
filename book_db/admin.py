from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Publisher)

admin.site.register(Creator)
admin.site.register(Subject)
admin.site.register(Book)