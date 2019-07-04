from rest_framework.pagination import PageNumberPagination
import json
from .serializers import InsertSerializer, BookSerializer
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response
from .models import Book, Publisher, Subject, Creator
import jdatetime
from rest_framework import status
import pyisbn
from django_filters import rest_framework as filters
from .date_filters import filter_date__exact, filter_date__gt, filter_date__lt
import requests


class GetAllBookCovers(GenericAPIView):
    def get_queryset(self):
        pass

    def get(self, request):

        print("Getting images...")

        books = Book.objects.all()

        print("Calculating Length...")
        l = len(books)

        print("Length is: %d" % l)

        part_size = l // 10

        ranges = [(part_size * i, (i+1) * part_size) for i in range(9)]
        ranges += [(9 * part_size, l)]

        for r in ranges:
            for id in range(r[0], r[1]):
                if books[id].image:
                    print("Getting Image For Book Id: %d ..." % books[id].id)
                    try:
                        f = open('media/book_cover/%d.jpg' % id, 'wb')
                        f.write(requests.get(books[id].image).content)
                        f.close()
                    except:
                        f = open('log.txt', 'a+')
                        f.write('%d\n' % id)
                        f.close()


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


class BookListFilterSet(filters.FilterSet):
    """
    Book filter set class
    filter a book by any of it's properties
    """

    issue_date = filters.DateFilter(method=filter_date__exact, field_name='issue_date', lookup_expr='exact')
    issue_date__gt = filters.DateFilter(method=filter_date__gt, field_name='issue_date', lookup_expr='gt')
    issue_date__lt = filters.DateFilter(method=filter_date__lt, field_name='issue_date', lookup_expr='lt')

    class Meta:
        model = Book
        fields = {
            'id': ['exact', ],
            'title': ['icontains', ],
            'publisher__name': ['icontains', ],
            'subjects__name': ['icontains', ],
            'creators__name': ['icontains', ],
            'isbn': ['icontains', ],
            'price': ['lt', 'gt'],
            'lang': ['icontains', ],
            'doe': ['icontains', ],
            'place': ['icontains', ],
            'edition': ['exact', 'lt', 'gt'],
            'volume': ['exact', 'lt', 'gt'],
            'isbn_clean': ['icontains', ],
        }


class BookList(ListAPIView):
    """
        An endpoint for a list of all books with
        filters
    """

    serializer_class = BookSerializer
    queryset = Book.objects.all().order_by('-issue_date')
    pagination_class = StandardResultsSetPagination
    filter_backends = (filters.DjangoFilterBackend, )
    filter_class = BookListFilterSet


class BookSearch(ListAPIView):
    """
        And endpoint for searching a book by an unspecified filed
        ** VERY SLOW **
    """

    pagination_class = StandardResultsSetPagination
    serializer_class = BookSerializer

    def get_queryset(self):
        query = self.request.query_params.get('query', None)

        if not query:
            return []

        results = []

        # by by id
        try:
            _id = int(query)
            results += Book.objects.filter(id=_id)
        except:
            pass

        # by title
        results += Book.objects.filter(title__icontains=query)

        # by publisher name
        for publisher in Publisher.objects.filter(name__icontains=query):
            results += publisher.books.all()

        # by creator name
        for creator in Creator.objects.filter(name__icontains=query):
            results += creator.books.all()

        # by subject
        for subject in Subject.objects.filter(name__icontains=query):
            results += subject.books.all()

        # by isbn
        try:
            # clean the query isbn first
            _isbn = query.replace('-', '')
            if len(_isbn) == 10:    # convert to isbn 13
                _isbn = pyisbn.convert(_isbn)

            results += Book.objects.filter(isbn_clean__icontains=_isbn)
        except:
            pass

        # by lang
        results += Book.objects.filter(lang__icontains=query)

        # by doe
        results += Book.objects.filter(doe__icontains=query)

        # by place
        results += Book.objects.filter(place__icontains=query)

        return results

