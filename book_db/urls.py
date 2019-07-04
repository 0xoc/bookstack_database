from django.urls import path
from .views import InsertView, BookList, BookSearch, GetAllBookCovers

urlpatterns = [
    path('insert/', InsertView.as_view()),
    path('list/', BookList.as_view()),
    path('search/', BookSearch.as_view()),
    path('get-all-book-covers/', GetAllBookCovers.as_view())
]
