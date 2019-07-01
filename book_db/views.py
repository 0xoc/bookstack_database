from .models import *
import json
from django.http import HttpResponse
from .serializers import InsertSerializer
from rest_framework.generics import GenericAPIView
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
            try:
                print(counter, len(books))

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

                    if book['subjects']:

                        for subject in book['subjects']:

                            try:
                                subject = Subject.objects.get(id=subject['id'])
                            except Subject.DoesNotExist:
                                subject = Subject.objects.create(id=subject['id'], name=subject['title'])

                            the_book.subjects.add(subject)

                    if book['authors']:
                        for creator in book['authors']:
                            try:
                                creator = Creator.objects.get(id=creator['id'])
                            except Creator.DoesNotExist:
                                creator = Creator.objects.create(id=creator['id'],
                                                                name=creator['name'],
                                                                type=creator['type'])
                            the_book.creators.add(creator)

                    the_book.save()
                    counter += 1
            except:
                raise Exception('book id: ' + book['book_id'])

        return Response({"Done": "done"})
