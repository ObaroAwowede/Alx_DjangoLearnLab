from django.urls import path, include
from .views import BookList, BookViewSet
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'books_all', BookViewSet, basename='book_all')
urlpatterns = [
    path('', include(router.urls)),
    path('books/', BookList.as_view(), name = 'book-list'),
]