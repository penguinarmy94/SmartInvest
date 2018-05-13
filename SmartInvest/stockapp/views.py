

from django.shortcuts import render
from django.http import HttpResponse

cards = [
{'header':'Invest','body':'','src':'/invest'},
{'header':'Portfolio','body':'','src':'/portfolio'},
{'header':'Trends','body':'','src':'/trends'},
{'header':'About','body':'','src':'/about'}
]


def home(request):
    return render(request, 'home.html',{'cards':cards})
def trends(request):
    return render(request, 'trends.html')
