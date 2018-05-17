from django.shortcuts import render
from django.http import HttpResponse
from myproject import settings
import json
import os

__file = open(os.path.join(settings.BASE_DIR, 'static/json/strategies.json'))
__loader = json.load(__file)
linksCards = __loader['linksCards']
teamsCards = __loader['teamsCards']

def home(request):
    return render(request, 'home.html',{'cards':linksCards})
def team(request):
    return render(request, 'about.html')
def about(request):
    return render(request, 'about.html',{'cards':teamsCards})
def services(request):
    return render(request, 'services.html')
