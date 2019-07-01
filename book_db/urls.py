from django.urls import path
from .views import InsertView

urlpatterns = [
    path('insert/', InsertView.as_view())
]
