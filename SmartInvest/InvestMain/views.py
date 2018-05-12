from django.shortcuts import render, redirect
from myproject import settings
from django.views.generic import TemplateView
from InvestMain.forms import *
from InvestMain.calculator import *
from InvestMain.helper import *
import json
import os

apihost = "https://api.iextrading.com/1.0/stock"
apihost_extension = "/realtime-update"

"""
	Loads the results from the stock calculator view
"""
def stock_portfolio(request):	
	return render(request, 'portfolio.html', { "data":  data})

def stock_invest_options(request):
	file = open(os.path.join(settings.BASE_DIR,'static/json/strategies.json'))
	strategy_json = json.load(file)
	strats = strategy_json["strategies"]
	
	if request.method == "GET":		
		return render(request, 'invest.html', strats)
	if request.method == "POST":		
		investment = InvestmentForm(request.POST or None)
		
		if investment.is_valid():
			data = investment.cleaned_data
			total_money = calc_total_invest(data)
						
			if total_money < 5000:
				print("Amount is less than $5000. Must invest a total of $5000")
				return render(request, 'invest.html', strats)
			
			strategies = get_strategies(data)
			stocks = []
			
			for val in strategies:
				stocks.append(all_stocks_to_invest(data,val))
			
			stock_count = invest_division(data, strategies, stocks, apihost, apihost_extension)
			
			data_stocks = {}
			data_array = []
			detail_array = []
			categories = []
			
			
			count = 0
			for stock_set in stocks:
				temp = []
				strategy = strategies[count]
				for i in range(len(stock_set)):
					
					value = stock_count[strategy][i]
					details = fetch_data_api(apihost, apihost_extension, stock_set[i])
					price = value*details["latestPrice"]
					name = details["companyName"] + "(" + stock_set[i] + ")"
					temp.append(price)
					categories.append(name)
					detail_array.append({"name": name, "y": price })
					data_array.append(details["latestPrice"])
				count += 1
			
			series = [{"name": "Stock Price", "data": data_array}]
			data_stocks["histo_data"] = series
			data_stocks["pie_data"] = detail_array
			data_stocks["histo_title"] = "Current Stock Values - " + date_time()
			data_stocks["pie_title"] = "Stock Portfolio - " + date_time()
			data_stocks["strategies"] = categories
			
			stock_count_array = []
			
			for key in stock_count:
				stock_count_array.append(stock_count[key])
			
			print(stock_count_array)
			return render(request, 'portfolio.html', {"data": json.dumps(data_stocks), "strategies": strategies, "stocks": stocks, "stock_count": stock_count_array, "length": len(strategies)})

			
		else:
			return redirect(stock_portfolio)
				
			
		return render(request, 'invest.html', strats)
		
		
