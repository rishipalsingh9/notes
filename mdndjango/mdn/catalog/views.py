from django.shortcuts import get_object_or_404
from django.views import generic
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
    
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genre': num_genre,
    }
    
    # Render the HTML template index.html with the data in context
    return render(request, 'catalog/index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10
    # your own name for the list as a template variable
    #context_object_name = 'my_book_list'
    #queryset = Book.objects.filter(title__icontains='power')[:5]  # Get 5 books containing the title power
    # Specify your own template name/location
    #template_name = 'books/my_arbitrary_template_name_list.html'

    """def get_queryset(self):
        # Get 5 books containing the title war
        return Book.objects.filter(title__icontains='power')[:5]

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(BookListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context
"""

class BookDetailView(generic.DetailView):
    model = Book