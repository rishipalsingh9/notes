from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from .forms import AuthorForm, BookForm
from . models import *

# Create your views here.

def authorform(request):
    if request.method == 'POST':
        fmat = AuthorForm(request.POST)
        if fmat.is_valid():
            nm = fmat.cleaned_data['name']
            tit = fmat.cleaned_data['title']
            bt = fmat.cleaned_data['birth_date']
            fmath = Author(name=nm, title=tit, birth_date=bt)
            fmath.save()
    
    else:
        fmat = AuthorForm()
    return render(request, 'rk001/addauthor.html', {'form' : fmat})


def bookform(request):
    if request.method == 'POST':
        fmbk = BookForm(request.POST)
        if fmbk.is_valid():
            nm = fmbk.cleaned_data['name']
            #aut = fmbk.cleaned_data['author']
            fmbks = Book(name=nm)
            #print(aut)
            fmbks.save()
            
    else:
        fmbk = BookForm()
    return render(request, 'rk001/addbook.html', {'form': fmbk})