from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import LibraryDetailView, UserRegistrationView, list_books

app_name = 'relationship_app'

urlpatterns = [
    path('libraries/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('books/', list_books, name='book_list'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logged_out.html'), name='logout'),
    path('admin/dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('librarian/dashboard/', views.librarian_dashboard_view, name='librarian_dashboard'),
    path('member/dashboard/', views.member_dashboard_view, name='member_dashboard'),
]