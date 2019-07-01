from django.db import models
from django_jalali.db import models as jmodels

class Publisher(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)

class Creator(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)

class Subject(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)

class Book(models.Model):
    id = models.PositiveIntegerField(primary_key=True) 
    title = models.CharField(max_length=2000, blank=True, null=True)
    
    publisher = models.ForeignKey(Publisher, related_name="books", on_delete=models.SET_NULL ,blank=True, null=True)
    
    subjects = models.ManyToManyField(Subject, related_name="books", blank=True)
    creators = models.ManyToManyField(Creator, related_name="books", blank=True)

    issue_date = jmodels.jDateField(blank=True, null=True)

    isbn = models.CharField(max_length=255, blank=True, null=True)
    price = models.PositiveIntegerField(blank=True, null=True)
    image = models.ImageField(max_length=255, blank=True, null=True)
    pdf = models.FileField(max_length=255, blank=True, null=True)
    page_count = models.PositiveIntegerField(blank=True, null=True)
    count = models.PositiveIntegerField(blank=True, null=True)
    isbn = models.CharField(max_length=255, blank=True, null=True)
    lang = models.CharField(max_length=255, blank=True, null=True)
    doe = models.CharField(max_length=255, blank=True, null=True)
    place = models.CharField(max_length=255, blank=True, null=True)


    def __str__(self):
        return str(self.title)