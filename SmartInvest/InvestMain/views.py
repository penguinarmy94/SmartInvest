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
	Shows a stock portfolio with the following:
		1. Table of all investment strategies, stocks, and allotment in each strategy
		2. Pie Chart of the total amount of money user has in each stock
		3. HIstogram of the current values of each stock in the strategies selected
"""
def stock_portfolio(request):

	# Check if the user is authenticated and if the http method is a GET request
	if request.method == "GET" and request.user.is_authenticated:	
		
		# Attempt to obtain values from the database
		try:
			stored = Strategy.objects.filter(userid = request.user) # stored Strategy objects
			stock_list = {}	# Holds Stock objects for all the stocks the user has invested in
			stock_price = [] # Holds the current total investment and gain for each stock at the currend date and time
			stock_info = []	# Holds the stock name for each of the stocks and their respective stock vallues at current data and time
			stock_names = [] # Holds the name of the stocks as strings
			js = {}	# Used for values on pie chart and histogram in Javascript
			
			# Gets all of the stocks per strategy that the user invested in
			for strategy in stored:
				stock_list[strategy.lookup] = get_stocks(strategy) 
				stock_list[strategy.lookup].append(strategy.name)
			
			# Updates the Stock objects with current values (name, current price, total price invested)
			for strategy in stored:
				# Stock 1
				gain = stock_list[strategy.lookup][0].price * strategy.number_of_stocks_1
				name = stock_list[strategy.lookup][0].name + "(" + stock_list[strategy.lookup][0].symbol + ")"
				stock_list[strategy.lookup][0].allotment = strategy.number_of_stocks_1
				stock_price.append(gain)
				stock_info.append({"name": name, "y": gain})
				stock_names.append(name)
				
				# Stock 2
				gain = stock_list[strategy.lookup][1].price * strategy.number_of_stocks_2
				name = stock_list[strategy.lookup][1].name + "(" + stock_list[strategy.lookup][1].symbol + ")"
				stock_list[strategy.lookup][1].allotment = strategy.number_of_stocks_2
				stock_price.append(gain)
				stock_info.append({"name": name, "y": gain})
				stock_names.append(name)
					
				# Stock 3
				gain = stock_list[strategy.lookup][2].price * strategy.number_of_stocks_2
				name = stock_list[strategy.lookup][2].name + "(" + stock_list[strategy.lookup][2].symbol + ")"
				stock_list[strategy.lookup][2].allotment = strategy.number_of_stocks_2
				stock_price.append(gain)
				stock_info.append({"name": name, "y": gain})
				stock_names.append(name)
				
			
			js["histo_title"] = "Current Stock Values - " + date_time() # Title of histogram
			js["strategies"] = stock_names # Categories for histogram
			js["pie_title"] = "Stock Portfolio - " + date_time() # Title of Pie Chart
			js["histo_data"] = [{"name": "Stock Price", "data": stock_price}] # Data used for filling out histogram (stock names and current price)
			js["pie_data"] = stock_info # Data used for filling out pie chart (stock names and current total for user)
			
			pattern = request.GET.get('status', '') # Checks for a status variable
			
			# If the status of the portfolio was updated
			if pattern == 'updated':
				return render(request, 'portfolio.html', { "status": 0, "stocks": stock_list, "js": json.dumps(js)})
			# If the status of the portfolio was created
			elif pattern == 'created':
				return render(request, 'portfolio.html', { "created": 1, "stocks": stock_list, "js": json.dumps(js)})
			# if the status of the portfolio does not exist
			else:
				return render(request, 'portfolio.html', { "status": 2, "stocks": stock_list, "js": json.dumps(js)})
		except ObjectDoesNotExist:
			# Portfolio does not exist, redirect to invest page
			return redirect("/invest")
	else:
		# Not a get request, redirect to signin page
		return redirect("/signin")
	
"""
	Shows investment options for the user to invest in
		1. Ethical Investment
		2. Growth Investment
		3. Index Investment
		4. Quality Investment
		5. Value Investment
		
	User can add an amount to any of the five strategies
	Total amount must be greater than or equal to $5000
"""
def stock_invest_options(request):
	
	# Get JSON stock info
	file = open(os.path.join(settings.BASE_DIR,'static/json/strategies.json'))
	invest_info = json.load(file)
	strats = invest_info["strategies"]
	
	# Check if the user has been authenticated
	if request.user.is_authenticated:
		
		# Check if the user is just trying to get the page
		if request.method == "GET":
			return render(request, 'invest.html', strats)
		
		# Check if the user is trying to invest 
		elif request.method == "POST":
			investment = InvestmentForm(request.POST or None)
			
			# Check amounts in investment strategies to invest
			if investment.is_valid():
				data = investment.cleaned_data
				total_money = calc_total_invest(data)
				
				# Do not follow through transaction if total investment amount is less than $5000
				if total_money < 5000:
					strats["alert"] = "Total amount of investment needs to be greater than $5000"
					strats["status"] = True
					return render(request, 'invest.html', strats)
				else:
					strategies = get_strategies(data, request.user) # Get investment strategies to invest in
					
					try:
						stored = Strategy.objects.filter(userid = request.user) # attempt to get previous investments for user
						update_strategies(stored, strategies)	# attempt to update the investments for the user
						return redirect("/portfolio?status=updated") # Show portfolio
						
					except ObjectDoesNotExist:
						for i in strategies:	# Create new investment data for the user
							i.save()
						
						return redirect("/portfolio?status=created") # Show portfolio
			else:
				strats["alert"] = "Some of the fields have non-numeric data. Only number values allowed"
				strats["status"] = True
				return render(request, 'invest.html', strats) 
				
		# Any other request route to home
		else:
			return redirect("/")
	else:
		return redirect("/signin")
		
""" Possible route for portfolio trend """
def portfolio_trend(request):
	
	# Check if user is authenticated
	if (request.user.is_authenticated):
		# Check if the user wants to see the trends
		if (request.method == "GET"):
			try:
				data = Strategy.objects.filter(request.user)
				strategies = []
				stocks = []
				stock_count = []
				
				for strat in data:
					shares = []
					strategies.append(strat.name)
					stocks.append(get_stocks(strat))
					shares.append(strat.number_of_stocks_1)
					shares.append(strat.number_of_stocks_2)
					shares.append(strat.number_of_stocks_3)
					stock_count.append(shares)
				
				
				"""
					strategies = [ 
							"Ethical Investment", 	# Only if user has invested in this strategy
							"Growth Investment", 	# Only if the user has invested in this strategy
							"Index Investment", 	# Only if user has invested in this strategy
							"Quality Investment",	# Only if user has invested in this strategy
							"Value Investment"	# Only if user has invested in this strategy
					]
					
					stocks = [
							["stock1", "stock2", "stock3"],	# Ethical Investment (if user has invested here)
							["stock1", "stock2", "stock3"],	# Growth Investment (if user has invested here)
							["stock1", "stock2", "stock3"],	# Index Investment (if user has invested here)
							["stock1", "stock2", "stock3"],	# Quality Investment (if user has invested here)
							["stock1", "stock2", "stock3"]	# Value Investment (if user has invested here)	
					]
					
					stock_num = [
							[1, 2, 3],	# Allotment in each of the stocks for Ethical Investment
							[4, 7, 9],	# Allotment in each of the stocks for Growth Investment
							[17,90,21],	# Allotment in each of the stocks for Index Investment
							[33,56,16],	# Allotment in each of the stocks for Quality Investment
							[45,67,88]	# Allotment in each of the stocks for Value Investment
					]
				
				"""
					
				return render(request, 'stock.html', {"strategies": strategies, "stocks": stocks, "stock_num": stock_count})
			except ObjectDoesNotExist:
			return redirect("/")
			
		# Route other requests to home
		else:
			return redirect("/")
	else:
		return redirect("/signin")
				
