from django.urls import path
from .views import LibraryDetail, list_books 

app_name = 'relationship_app'

urlpatterns = [
    path('libraries/<int:pk>/', LibraryDetail.as_view(), name='library_detail'),
    path('books/', list_books, name='book_list'),
]