

from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'home.html')
def trends(request):
    return render(request, 'trends.html')
