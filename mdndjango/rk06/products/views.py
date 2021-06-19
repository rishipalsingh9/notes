from django.shortcuts import render
from . models import *
# Create your views here.


def index(request):
    return render(request, 'products/index.html')


def agent(request):
    agent_data = Agent.objects.all()
    return render(request, 'products/agent.html', {'agents': agent_data})


def supplier(request):
    supplier_data = Supplier.objects.all()
    return render(request, 'products/supplier.html', {'suppliers': supplier_data})


def hotel(request):
    hotel_data = Accommodation.objects.all()
    return render(request, 'products/hotel.html', {'accommodations': hotel_data})