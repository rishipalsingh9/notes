from django.shortcuts import render
from . models import *
# Create your views here.


def index(request):
    return render(request, 'rk04/index.html')

def notes(request):
    return render(request, 'rk04/notes.html')

def agents(request):
    a_name = Agent.objects.all()
    context = {'agency_name': a_name}
    return render(request, 'rk04/agents.html', context)
    