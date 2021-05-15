from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.http import HttpResponse
from django.shortcuts import render
from catalog.models import *  # star stands for importing all models from catalog.models

# Create your views here.


def index(request):
    """ Views function for home page of site."""
    # Generate count of some of obj. from models.py
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_genre = Genre.objects.all()
    
    #Available bookes (status = 'avail')
    num_instances_available = BookInstance.objects.filter(status__exact='avail').count()
    
    #The 'all()' is implied by default
    num_authors = Author.objects.count()
    
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1
    
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genre': num_genre,
        'num_visits': num_visits,
    }
    
    # Render the HTML template index.html with the data in context
    return render(request, 'catalog/index.html', context=context)


class BookListView(ListView):
    model = Book
    # your own name for the list as a template variable
    #context_object_name = 'my_book_list'
    #queryset = Book.objects.filter(title__icontains='power')[:5]  # Get 5 books containing the title power
    # Specify your own template name/location
    #template_name = 'books/my_arbitrary_template_name_list.html'

    """def get_queryset(self):
        # Get 5 books containing the title war
        return Book.objects.filter(title__icontains='power')[:5]
    """
    """
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(BookListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context
    """
    
class BookDetailView(DetailView):
    model = Book
    
class AuthorListView(ListView):
    model = Author
    
class AuthorDetailView(DetailView):
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin, ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class LoanedBooksAllListView(PermissionRequiredMixin, ListView):
    """Generic class-based view listing all books on loan. Only visible to users with can_mark_returned permission."""
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')
