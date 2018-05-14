from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from myproject import settings
from django.views.generic import TemplateView
from InvestMain.forms import *
from InvestMain.calculator import *
from InvestMain.helper import *
from InvestMain.models import Strategy
import json
import os

apihost = "https://api.iextrading.com/1.0/stock"
apihost_extension = "/realtime-update"

"""
	Loads the results from the stock calculator view
"""
def stock_portfolio(request):
	if request.method == "GET" and request.user.is_authenticated:	

		try:
			stored = Strategy.objects.filter(userid = request.user)
			stock_list = {}
			stock_price = []
			stock_info = []
			stock_names = []
			js = {}
			
			js["histo_day"] = []
			for strategy in stored:
				stock_list[strategy.lookup] = get_stocks(strategy) 
				stock_list[strategy.lookup].append(strategy.name)
			
			for strategy in stored:
				gain = stock_list[strategy.lookup][0].price * strategy.number_of_stocks_1
				name = stock_list[strategy.lookup][0].name + "(" + stock_list[strategy.lookup][0].symbol + ")"
				stock_list[strategy.lookup][0].allotment = strategy.number_of_stocks_1
				stock_price.append(gain)
				stock_info.append({"name": name, "y": gain})
				stock_names.append(name)
				
				gain = stock_list[strategy.lookup][1].price * strategy.number_of_stocks_2
				name = stock_list[strategy.lookup][1].name + "(" + stock_list[strategy.lookup][1].symbol + ")"
				stock_list[strategy.lookup][1].allotment = strategy.number_of_stocks_2
				stock_price.append(gain)
				stock_info.append({"name": name, "y": gain})
				stock_names.append(name)
								
				gain = stock_list[strategy.lookup][2].price * strategy.number_of_stocks_2
				name = stock_list[strategy.lookup][2].name + "(" + stock_list[strategy.lookup][2].symbol + ")"
				stock_list[strategy.lookup][2].allotment = strategy.number_of_stocks_2
				stock_price.append(gain)
				stock_info.append({"name": name, "y": gain})
				stock_names.append(name)
				
			
			js["histo_title"] = "Current Stock Values - " + date_time()
			js["strategies"] = stock_names
			js["pie_title"] = "Stock Portfolio - " + date_time()
			js["histo_data"] = [{"name": "Stock Price", "data": stock_price}]
			js["pie_data"] = stock_info
			
			pattern = request.GET.get('status', '')
			if pattern == 'updated':
				return render(request, 'portfolio.html', { "status": 0, "stocks": stock_list, "js": json.dumps(js)})
			elif pattern == 'created':
				return render(request, 'portfolio.html', { "created": 1, "stocks": stock_list, "js": json.dumps(js)})
			else:
				return render(request, 'portfolio.html', { "status": 2, "stocks": stock_list, "js": json.dumps(js)})
		except ObjectDoesNotExist:
			return redirect("/")
	else:
		return redirect("/")
	

def stock_invest_options(request):
	file = open(os.path.join(settings.BASE_DIR,'static/json/strategies.json'))
	invest_info = json.load(file)
	strats = invest_info["strategies"]
	
	if request.user.is_authenticated:
	
		if request.method == "GET":
			return render(request, 'invest.html', strats)
			
		elif request.method == "POST":
			investment = InvestmentForm(request.POST or None)
		
			if investment.is_valid():
				data = investment.cleaned_data
				total_money = calc_total_invest(data)
						
				if total_money < 5000:
					strats["alert"] = "Total amount of investment needs to be greater than $5000"
					strats["status"] = True
					return render(request, 'invest.html', strats)
				else:
					strategies = get_strategies(data, request.user)
					
					try:
						stored = Strategy.objects.filter(userid = request.user)
						update_strategies(stored, strategies)
						return redirect("/portfolio?status=updated")
						
					except ObjectDoesNotExist:
						for i in strategies:
							i.save()
						
						return redirect("/portfolio?status=created")
			else:
				strats["alert"] = "Fields cannoot be left blank"
				strats["status"] = True
				return render(request, 'invest.html', strats) 
		else:
			return redirect("/")
	else:
		return redirect("/")
		
""" Possible route for portfolio trend """
def portfolio_trend(request):
	strategies = ["ethical", "growth", "index", "quality", "value"]
	stocks = [
			["stock1", "stock2", "stock3"],
			["stock4", "stock5", "stock6"],
			["stock7", "stock8", "stock9"],
			["stock10", "stock11", "stock12"],
			["stock13", "stock14", "stock15"]
		]
	stock_count = {
			[1, 2, 4],
			[6, 5, 4],
			[6, 7, 6],
			[7, 7, 8],
			[1, 1, 1]
	}
	
	return render(request, 'invest.html', {"strategies": strategies, "stocks": stocks, "stock_num": stock_count})
