from django.urls import path
from .views import InsertView, BookList

urlpatterns = [
    path('insert/', InsertView.as_view()),
    path('list/', BookList.as_view())
]
