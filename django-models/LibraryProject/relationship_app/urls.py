from django.urls import path
from .views import LibraryDetailView, UserRegistrationView, UserLoginView, UserLogoutView
from .views import list_books


app_name = 'relationship_app'

urlpatterns = [
    path('libraries/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('books/', list_books, name='book_list'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]