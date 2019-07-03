import django_filters
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from .models import *
import json
from .serializers import InsertSerializer, BookSerializer
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response
from .models import *
import jdatetime
from rest_framework import status
import pyisbn


class InsertView(GenericAPIView):
    serializer_class = InsertSerializer

    def get_queryset(self):
        pass

    @staticmethod
    def post(request):
        """
        receives a json file and creates book objects
        :param request:
        :return:
        """

        json_file = request.FILES.get('json_file', None)

        if not json_file:
            return Response({"error": "No files"}, status=status.HTTP_400_BAD_REQUEST)

        # open the json file and decode as uft-8
        f = open(json_file.temporary_file_path(), 'r', encoding='utf-8')

        # convert json to python dictionary
        books = json.loads(f.read())

        # used to show progress
        counter = 0

        for book in books:
            # show progress
            if counter % 10000 == 0:
                print(counter, len(books))

            try:

                try:  # if the book exists dont' go through converting json
                    Book.objects.get(id=book['book_id'])
                except Book.DoesNotExist:
                    print("new book")
                    title = book['title']
                    book_id = book['book_id']
                    isbn = book['isbn']
                    image = book['image_link']
                    pdf = book['pdf_link']
                    page_count = book['pages']
                    edition = book['edition']
                    count = book['count']
                    lang = book['lang']
                    doe = book['doe']
                    place = book['place']
                    issue_date_str = book['issue_date']
                    volume = book['volume']

                    # clean isbn does not have '-' and is converted to isbn 13
                    isbn_clean = book['isbn'].replace('-', '')
                    if len(isbn_clean == 10):
                        try:
                            isbn_clean = pyisbn.convert(isbn_clean)
                        except:
                            pass

                    try:  # issue date might be blank or in wrong format
                        date = issue_date_str.split('/')
                        date[0] = '13' + date[0]

                        issue_date = jdatetime.date(int(date[0]), int(date[1]), int(date[2]))
                    except:  # if no valid issue_date found, set that to None
                        issue_date = None

                    try:  # price might be blank or in the wrong format
                        price = int(book['price'])
                    except:  # set None if no valid price
                        price = None

                    if book['publisher']:  # if book has publisher available
                        try:
                            # if publisher already in database

                            publisher = Publisher.objects.get(id=book['publisher']['id'])

                        except Publisher.DoesNotExist:

                            # if publisher not in database, create it
                            publisher = Publisher.objects.create(id=book['publisher']['id']
                                                                 , name=book['publisher']['name'])
                    else:                  # if no publisher available set it to None
                        publisher = None

                    # construct the book object
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
                        volume=volume,
                        isbn_clean=isbn_clean
                    )

                    the_book.save()

                    try:    # subjects may not be present

                        for subject in book['subjects']:
                            # get to create subject objects

                            try:
                                subject = Subject.objects.get(id=subject['id'])
                            except Subject.DoesNotExist:
                                subject = Subject.objects.create(id=subject['id'], name=subject['title'])

                            the_book.subjects.add(subject)
                    except:
                        pass

                    try:    # creators may not be present
                        for creator in book['authors']:
                            # get or create, creators

                            try:
                                creator = Creator.objects.get(id=creator['id'])
                            except Creator.DoesNotExist:
                                creator = Creator.objects.create(id=creator['id'],
                                                                 name=creator['name'],
                                                                 type=creator['type'])
                            the_book.creators.add(creator)
                    except:
                        pass

                    # save the book object into database
                    the_book.save()
            except:
                # if any uncut exception occur raise it with the book id that caused it
                raise Exception('book id: ' + book['book_id'])

            counter += 1

        return Response({"status": "done"})


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 100


class BookList(ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        qs = self.request.GET.get('qs', None)

        if qs:
            qs1 = Book.objects.filter(Q(title__icontains=qs) |
                                      Q(isbn__icontains=qs) |
                                      Q(lang__icontains=qs)
                                      ).distinct()
            qs2 = Book.objects.filter(creators__name__icontains=qs)
            qs3 = Book.objects.filter(publisher__name__icontains=qs)
            qs4 = Book.objects.filter(subjects__name__icontains=qs)
            return qs1.union(qs2).union(qs3).union(qs4).order_by('-issue_date')
        return Book.objects.all().order_by('-issue_date')

    pagination_class = StandardResultsSetPagination
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = ('title', 'publisher', 'creators__name', 'subjects__name', 'isbn_clean')


class BookFieldSearch(ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):

        # get search parameter

        id = self.request.GET.get('id', None)
        title = self.request.GET.get('title', None)
        publisher = self.request.GET.get('publisher', None)

        # todo : subjects as list
        subjects = self.request.GET.get('subjects', None)

        # todo : creators as list
        creators = self.request.GET.get('creators', None)

        # todo: date range
        issue_date = self.request.GET.get('issue_date', None)

        isbn = self.request.GET.get('isbn', None)

        # todo: price as range
        price = self.request.GET.get('price', None)

        # todo: page count as range
        # todo: count as range

        lang = self.request.GET.get('lang', None)
        doe = self.request.GET.get('doe', None)
        place = self.request.GET.get('place', None)
        edition = self.request.GET.get('edition', None)
        volume = self.request.GET.get('volume', None)
        isbn_clea = self.request.GET.get('isbn_clean', None)
