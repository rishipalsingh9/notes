from django.http import HttpResponse
from django.shortcuts import render
from catalog.models import *  # star stands for importing all models from catalog.models

# Create your views here.


def index(request):
    """ Views function for home page of site."""
    # Generate count of some of obj. from models.py
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    
    #Available bookes (status = 'avail')
    num_instances_available = BookInstance.objects.filter(status__exact='avail').count()
    
    #The 'all()' is implied by default
    num_authors = Author.objects.count()
    
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }
    
    # Render the HTML template index.html with the data in context
    return render(request, 'catalog/index.html', context=context)
    