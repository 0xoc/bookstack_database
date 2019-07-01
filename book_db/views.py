from .models import *
import json
from django.http import HttpResponse
from .serializers import InsertSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .models import *

class InsertView(GenericAPIView):
    serializer_class = InsertSerializer

    def get_queryset(self):
        pass

    def post(self, request):
        json_file = request.FILES['json_file']

        f = open(json_file.temporary_file_path(), 'r', encoding='utf-8')
        books = json.loads(f.read())

        for book in books:
            try:
                book = Book.objects.get(id=book['book_id'])
            except Book.DoesNotExist:

                title = book['title']
                book_id = book['book_id']
                isbn = book['isbn']

                try:
                    publisher = Publisher.objects.get(id=book['publisher']['id'])
                except Publisher.DoesNotExist:
                    publisher = Publisher.objects.create(id=book['publisher']['id']
                                        ,name=book['publisher']['name'])

                for subject in book['subjects']:

                    try:
                        subject = Subject.objects.get(id=subject['id'])
                    except Subject.DoesNotExist:
                        subject = Subject.objects.create(id=subject['id'], name=subject['title'])

                for creator in book['authors']:
                    try:
                        creator = Creator.objects.get(id=creator['id'])
                    except Creator.DoesNotExist:
                        creator = Creator.objects.create(id=creator['id'],
                                                        name=creator['name'],
                                                        type=creator['type'])
            
        return Response({"Done": "done"})
