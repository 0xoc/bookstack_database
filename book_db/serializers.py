from rest_framework import serializers
from .models import *

class InsertSerializer(serializers.Serializer):
    json_file = serializers.FileField()


class CreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creator
        fields = ['id', 'name', 'type']


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['id', 'name']


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name']


class BookSerializer(serializers.ModelSerializer):
    creators = CreatorSerializer(many=True)
    subjects = SubjectSerializer(many=True)
    publisher = PublisherSerializer()

    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'publisher',
            'subjects',
            'creators',
            'issue_date',
            'isbn',
            'price',
            'image',
            'pdf',
            'page_count',
            'count',
            'lang',
            'doe',
            'place',
            'edition',
            'volume',
            'isbn_clean'
        ]

