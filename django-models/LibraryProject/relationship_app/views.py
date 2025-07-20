from django.shortcuts import render
from .models import Library
from django.contrib.auth.decorators import user_passes_test, permission_required
from .models import Book, Author, Librarian
from django.views.generic.detail import DetailView
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from django.contrib.auth import login 
from django.contrib.auth.forms import UserCreationForm 
from django import forms
from django.utils.decorators import method_decorator

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author']

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('relationship_app:login')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


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


def is_admin(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

@user_passes_test(is_admin, login_url='/login/')
def admin_dashboard_view(request):
    return render(request, 'relationship_app/admin_view.html', {'user': request.user})

@user_passes_test(is_librarian, login_url='/login/')
def librarian_dashboard_view(request):
    return render(request, 'relationship_app/librarian_view.html', {'user': request.user})

@user_passes_test(is_member, login_url='/login/')
def member_dashboard_view(request):
    return render(request, 'relationship_app/member_view.html', {'user': request.user})

@method_decorator(permission_required('relationship_app.can_add_book', login_url='/login/'), name='dispatch')
class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'relationship_app/book_form.html'
    success_url = reverse_lazy('relationship_app:book_list')

@method_decorator(permission_required('relationship_app.can_change_book', login_url='/login/'), name='dispatch')
class BookUpdateView(UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'relationship_app/book_form.html'
    context_object_name = 'book'
    success_url = reverse_lazy('relationship_app:book_list')

@method_decorator(permission_required('relationship_app.can_delete_book', login_url='/login/'), name='dispatch')
class BookDeleteView(DeleteView):
    model = Book
    template_name = 'relationship_app/book_confirm_delete.html'
    context_object_name = 'book'
    success_url = reverse_lazy('relationship_app:book_list')
