from django.shortcuts import render
from .models import Library
from django.contrib.auth.decorators import user_passes_test
from .models import Book, Author, Librarian
from django.views.generic.detail import DetailView
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from django.contrib.auth import login 
from django.contrib.auth.forms import UserCreationForm 

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
    """Checks if the user is authenticated and has the 'Admin' role."""
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    """Checks if the user is authenticated and has the 'Librarian' role."""
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    """Checks if the user is authenticated and has the 'Member' role."""
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

# --- Role-Based Dashboard Views ---

@user_passes_test(is_admin, login_url='/login/')
def admin_dashboard_view(request):
    """View for Admin users."""
    return render(request, 'relationship_app/admin_view.html', {'user': request.user})

@user_passes_test(is_librarian, login_url='/login/')
def librarian_dashboard_view(request):
    """View for Librarian users."""
    return render(request, 'relationship_app/librarian_view.html', {'user': request.user})

@user_passes_test(is_member, login_url='/login/')
def member_dashboard_view(request):
    """View for Member users."""
    return render(request, 'relationship_app/member_view.html', {'user': request.user})