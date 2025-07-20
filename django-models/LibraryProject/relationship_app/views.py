from django.shortcuts import render
from .models import Library
from .models import Book, Author, Librarian
from django.views.generic.detail import DetailView
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from django.contrib.auth import login 
from django.contrib.auth.forms import UserCreationForm 


def list_books(request):
    books = Book.objects.all()
    context = {'list_books': books}
    return render(request,'relationship_app/list_books.html',context)

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["books"] = self.object.books.all()
        return context

class UserRegistrationView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('relationship_app:login') 


class UserLoginView(LoginView):
    template_name = 'login.html' 
   
class UserLogoutView(LogoutView):
    template_name = 'logout.html'
