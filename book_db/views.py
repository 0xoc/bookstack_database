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
            title = book['title']

            try:
                publisher = Publisher.objects.get(id=book['publisher']['id'])
            except Publisher.DoesNotExist:
                publisher = Publisher.objects.create(id=book['publisher']['id']
                                    ,name=book['publisher']['name'])

        return Response({"Done": "done"})
