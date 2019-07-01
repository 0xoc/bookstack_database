import sys
from collections import OrderedDict

import django_filters
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.functional import cached_property
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters

from .models import *
import json
from django.http import HttpResponse
from .serializers import InsertSerializer, BookSerializer
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response
from .models import *
import jdatetime

class InsertView(GenericAPIView):
    serializer_class = InsertSerializer

    def get_queryset(self):
        pass

    def post(self, request):
        print("hello post")

        json_file = request.FILES['json_file']

        f = open(json_file.temporary_file_path(), 'r', encoding='utf-8')
        books = json.loads(f.read())

        counter = 0
        
        for book in books:

            if counter % 100 == 0:
                print(counter, len(books))

            try:

                try:
                    book = Book.objects.get(id=book['book_id'])
                except Book.DoesNotExist:

                    title = book['title']
                    book_id = book['book_id']
                    isbn = book['isbn']

                    issue_date_str = book['issue_date']
                    try:
                        date = issue_date_str.split('/')
                        date[0] = '13' + date[0]

                        issue_date = jdatetime.date(int(date[0]), int(date[1]), int(date[2]))
                    except:
                        issue_date = None

                    try:
                        price = int(book['price'])
                    except:
                        price = None

                    image = book['image_link']
                    pdf = book['pdf_link']

                    page_count = book['pages']
                    edition = book['edition']

                    count = book['count']
                    lang = book['lang']
                    doe = book['doe']
                    place = book['place']

                    if book['publisher']:
                        try:
                            publisher = Publisher.objects.get(id=book['publisher']['id'])
                        except Publisher.DoesNotExist:
                            publisher = Publisher.objects.create(id=book['publisher']['id']
                                                ,name=book['publisher']['name'])
                    else:
                        publisher = None

                    the_book = Book(
                        title=title,
                        publisher=publisher,
                        id=book_id,
                        isbn=isbn,
                        issue_date=issue_date,
                        price=price,
                        image=image,
                        pdf=pdf,
                        page_count=page_count,
                        edition=edition,
                        count=count,
                        lang=lang,
                        place=place,
                        doe=doe,
                        )

                    the_book.save()

                    try:

                        for subject in book['subjects']:

                            try:
                                subject = Subject.objects.get(id=subject['id'])
                            except Subject.DoesNotExist:
                                subject = Subject.objects.create(id=subject['id'], name=subject['title'])

                            the_book.subjects.add(subject)
                    except:
                        pass

                    try:
                        for creator in book['authors']:
                            try:
                                creator = Creator.objects.get(id=creator['id'])
                            except Creator.DoesNotExist:
                                creator = Creator.objects.create(id=creator['id'],
                                                                name=creator['name'],
                                                                type=creator['type'])
                            the_book.creators.add(creator)
                    except:
                        pass

                    the_book.save()
            except:
                raise Exception('book id: ' + book['book_id'])

            counter += 1

        return Response({"Done": "done"})


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000


class CustomPaginatorClass(Paginator):
    @cached_property
    def count(self):
        return len(self.object_list)
        # return sys.maxsize

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 100
    # django_paginator_class = CustomPaginatorClass

    # def get_paginated_response(self, data):
    #     return Response(OrderedDict([
    #         ('next', self.get_next_link()),
    #         ('previous', self.get_previous_link()),
    #         ('results', data)
    #     ]))

class BookList(ListAPIView):
    serializer_class = BookSerializer
    def get_queryset(self):
        qs = self.request.GET.get('qs', None)
        if qs:
            qs1 = Book.objects.filter(Q(title__icontains=qs)|
                                      Q(isbn__icontains=qs)
                                      ).distinct()
            qs2 = Book.objects.filter(creators__name__icontains=qs)
            return qs1.union(qs2)
        return Book.objects.all()
    pagination_class = StandardResultsSetPagination
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    # filter_backends = (filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend)
    filterset_fields = ('title',)
    # search_fields = ['isbn', 'title', 'creators__name']



