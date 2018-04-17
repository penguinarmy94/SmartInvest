from django.shortcuts import render
from django.views.generic import TemplateView
from SmartInvest.forms import *


def stock_calculator(request):
	return render(request, 'stock.html', {})

def stock_portfolio(request):
	message = "Failure"
	if request.method == "POST":
		stock_request = StockCalculatorForm(request.POST)
		
		if not stock_request.is_valid():
			message = message + " " + stock_request.cleaned_data['symbol']
	else:
		stock_request = forms.StockCalculatorForm()
	
	return render(request, 'portfolio.html', { "message" : message})

# Create your views here.
