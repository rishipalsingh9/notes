from django.http import HttpResponseRedirect
from .forms import NameForm, ContactForm, AuthorForm
from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail


# Create your views here.

# def index(request):
# return HttpResponse("Welcome to MDN Tutorial")

def get_hello(request):
    user_name = request.POST.get('user_name', '')
    email = request.POST.get('email', '')
    if request.method == 'POST' and email and user_name:
        send_mail('Subject', 'Email message', 'info.europeous@gmail.com', ['info@europeoustours.com'],
                  fail_silently=False, )
        form = NameForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/thanks/')
    else:
        form = NameForm()
    return render(request, 'mdntuto/hello.html', {'form': form})


# def thanks (request):
#   return render(request, 'mdntuto/thanks.html')

def get_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/contacts/')
    else:
        form = ContactForm()
    return render(request, 'mdntuto/contact.html', {'form': form})


def get_article(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/articles/')
    else:
        form = AuthorForm()
    return render(request, 'mdntuto/article.html', {'form': form})
