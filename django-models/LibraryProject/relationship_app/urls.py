from django.urls import path
from django.contrib.auth import views as auth_views
from .views import LibraryDetailView, UserRegistrationView
from .views import list_books
from .views import register
from .views import admin_dashboard_view
from .views import librarian_dashboard_view
from .views import member_dashboard_view, BookCreateView, BookDeleteView, BookUpdateView
from . import views

app_name = 'relationship_app'
urlpatterns = [
    path('libraries/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
    path('books/', views.list_books, name='book_list'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logged_out.html'), name='logout'),
    path('admin/dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('librarian/dashboard/', views.librarian_dashboard_view, name='librarian_dashboard'),
    path('member/dashboard/', views.member_dashboard_view, name='member_dashboard'),
    path('books/<int:pk>/edit/', views.BookUpdateView.as_view(), name='edit_book'),
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='delete_book'),
    path('books/add/', views.BookCreateView.as_view(), name='add_book'),
]