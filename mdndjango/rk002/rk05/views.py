from django.shortcuts import render
from . forms import *

# Create your views here.

def index(request):
    return render(request, 'rk05/index.html')

def addagent(request):
    if request.method == 'POST':
        aa = AddAgent(request.POST)
        if aa.is_valid():
            name = aa.cleaned_data['agency_name']
            add = aa.cleaned_data['agency_address']
            city = aa.cleaned_data['city']
            pcode = aa.cleaned_data['postal_code']
            cunt = aa.cleaned_data['country']
            email = aa.cleaned_data['agent_email']
            cell = aa.cleaned_data['phone_number']
            print(name)
            print(add)
            print(city)
            print(pcode)
            print(cunt)
            print(email)
            print(cell)
            aa.save()
            
    else:
        aa = AddAgent()
    return render(request, 'rk05/addagent.html', {'form': aa})
