from django.urls import path
from .views import InsertView, BookList, BookSearch

urlpatterns = [
    path('insert/', InsertView.as_view()),
    path('list/', BookList.as_view()),
    path('search/', BookSearch.as_view())
]
