from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from .forms import TourPackages, CreateAgents
from . models import *

# Create your views here.


def register(request):
    if request.method == 'POST':
        fm = TourPackages(request.POST)
        if fm.is_valid():
            ptitle = fm.cleaned_data['tour_name']
            tnight = fm.cleaned_data['no_of_nights']
            tdate = fm.cleaned_data['travel_date']
            tend = fm.cleaned_data['end_date']
            titin = fm.cleaned_data['detail_itinerary']
            print(ptitle)
            print(tnight)
            print(tdate)
            print(tend)
            print(titin)
            fm.save()

    else:
        fm = TourPackages()
    return render(request, 'myappforms/packageregister.html', {'form': fm})


def createagent(request):
    if request.method == 'POST':
        fmag = CreateAgents(request.POST)
        if fmag.is_valid():
            agnm = fmag.cleaned_data['agency_name']
            anm = fmag.cleaned_data['prop_name']
            em = fmag.cleaned_data['email_agent']
            agad = fmag.cleaned_data['agency_address']
            agco = fmag.cleaned_data['contact_no']
            agct = fmag.cleaned_data['city']
            agcy = fmag.cleaned_data['country']
            fmagn = Agents(agency_name=agnm, prop_name=anm, email_agent=em,
                           agency_address=agad, contact_no=agco, city=agct, country=agcy)
            fmagn.save()

    else:
        fmag = CreateAgents()
    return render(request, 'myappforms/addagent.html', {'form': fmag})


#print(agnm)
#print(anm)
#print(em)
#print(agad)
#print(agco)
# print(agct)
# print(agcy)
