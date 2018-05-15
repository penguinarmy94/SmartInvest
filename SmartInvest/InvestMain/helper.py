import requests, datetime, time, socket, os, json
from myproject import settings
from InvestMain.models import Strategy
from InvestMain.classes import Stock
from django.shortcuts import render, redirect

__file = open(os.path.join(settings.BASE_DIR,'static/json/strategies.json'))
__strategy_json = json.load(__file)
__stocks = __strategy_json["stocks"]
__apihost = "https://api.iextrading.com/1.0/stock"
__apihost_extension = "/realtime-update"

""" 
	Calculates the total amount of investment
"""
def calc_total_invest(data):
	money = 0;
	if(data["ethical_invest"] > 0):
		money += data["ethical_invest"]
	if(data["growth_invest"] > 0):
		money += data["growth_invest"]
	if(data["index_invest"] > 0):
		money += data["index_invest"]
	if(data["quality_invest"] > 0):
		money += data["quality_invest"]
	if(data["value_invest"] > 0):
		money += data["value_invest"]
	
	return money

"""
	Gets the list of all strategies as strings
"""
def get_strategy_list():
	return ["Ethical Investment", "Growth Investment", "Index Investment", "Quality Investment", "Value Investment"]

"""
	Gets all strategies user wants to invest in as Strategy objects
"""	
def get_strategies(data, user):
	strategies = []
	
	if(data["ethical_invest"] > 0):
		stocks = []
		stocks.append(Stock(symbol = __stocks["ethical_invest"][0], shares = 0))
		stocks.append(Stock(symbol = __stocks["ethical_invest"][1], shares = 0))
		stocks.append(Stock(symbol = __stocks["ethical_invest"][2], shares = 0))
		
		stocks = __invest(data["ethical_invest"], stocks)
			
		strategies.append(Strategy(userid = user, lookup = "ethical_invest", name = "Ethical Investment", number_of_stocks_1 = stocks[0].allotment, number_of_stocks_2 = stocks[1].allotment, number_of_stocks_3 = stocks[2].allotment))
	if(data["growth_invest"] > 0):
		stocks = []
		stocks.append(Stock(symbol = __stocks["growth_invest"][0], shares = 0))
		stocks.append(Stock(symbol = __stocks["growth_invest"][1], shares = 0))
		stocks.append(Stock(symbol = __stocks["growth_invest"][2], shares = 0))
		
		stocks = __invest(data["growth_invest"], stocks)
			
		strategies.append(Strategy(userid = user, lookup = "growth_invest", name = "Growth Investment", number_of_stocks_1 = stocks[0].allotment, number_of_stocks_2 = stocks[1].allotment, number_of_stocks_3 = stocks[2].allotment))
	if(data["index_invest"] > 0):
		stocks = []
		stocks.append(Stock(symbol = __stocks["index_invest"][0], shares = 0))
		stocks.append(Stock(symbol = __stocks["index_invest"][1], shares = 0))
		stocks.append(Stock(symbol = __stocks["index_invest"][2], shares = 0))
		
		stocks = __invest(data["index_invest"], stocks)
			
		strategies.append(Strategy(userid = user, lookup = "index_invest", name = "Index Investment", number_of_stocks_1 = stocks[0].allotment, number_of_stocks_2 = stocks[1].allotment, number_of_stocks_3 = stocks[2].allotment))
	if(data["quality_invest"] > 0):
		stocks = []
		stocks.append(Stock(symbol = __stocks["quality_invest"][0], shares = 0))
		stocks.append(Stock(symbol = __stocks["quality_invest"][1], shares = 0))
		stocks.append(Stock(symbol = __stocks["quality_invest"][2], shares = 0))
		
		stocks = __invest(data["quality_invest"], stocks)
			
		strategies.append(Strategy(userid = user, lookup = "quality_invest", name = "Quality Investment", number_of_stocks_1 = stocks[0].allotment, number_of_stocks_2 = stocks[1].allotment, number_of_stocks_3 = stocks[2].allotment))
	if(data["value_invest"] > 0):
		stocks = []
		stocks.append(Stock(symbol = __stocks["value_invest"][0], shares = 0))
		stocks.append(Stock(symbol = __stocks["value_invest"][1], shares = 0))
		stocks.append(Stock(symbol = __stocks["value_invest"][2], shares = 0))
		
		stocks = __invest(data["value_invest"], stocks)
			
		strategies.append(Strategy(userid = user, lookup = "value_invest", name = "Value Investment", number_of_stocks_1 = stocks[0].allotment, number_of_stocks_2 = stocks[1].allotment, number_of_stocks_3 = stocks[2].allotment))
	
	return strategies

"""
	Gets all of the stock names belonging to a strategy (as strings)
"""
def get_stocks(strategy):
	stocks = []
	strat_name = ""
	if strategy.name == "Ethical Investment":
		strat_name = "ethical_invest"
	elif strategy.name == "Growth Investment":
		strat_name = "growth_invest"
	elif strategy.name == "Index Investment":
		strat_name = "index_invest"
	elif strategy.name == "Quality Investment":
		strat_name = "quality_invest"
	elif strategy.name == "Value Investment":
		strat_name = "value_invest"
	else:
		return stocks
		
	for stock in __stocks[strat_name]:
		data = fetch_data_api(__apihost, __apihost_extension, stock)
		a_stock = Stock(symbol = stock, shares = 0)
		a_stock.name = data["companyName"]
		a_stock.price = data["latestPrice"]
		
		stocks.append(a_stock)
		
	return stocks


"""
	Updates the strategies that the user has already invested in
"""
def update_strategies(stored, strategies):
	for i in stored:
		for j in strategies:
			if i.name == j.name:
				i.number_of_stocks_1 += j.number_of_stocks_1
				i.number_of_stocks_2 += j.number_of_stocks_2
				i.number_of_stocks_3 += j.number_of_stocks_3
				i.save()
	
	for i in strategies:
		bool = False
		for j in stored:
			if (i.name == j.name):
				bool = True
				break
		if not bool:
			i.save()

"""
	Splits the amount of money to invest into the stocks in the investment strategy
"""			
def __invest(amount, stocks):
	count = 0
	index = 0
	size = len(stocks)
	
	for i in range(size):
		data = fetch_data_api(__apihost, __apihost_extension, stocks[i].symbol)
		stocks[i].price = data["latestPrice"]
		stocks[i].name = data["companyName"]
		
	while (amount >= 0 and count < size) or count < size:
		if stocks[index].price <= amount:
			stocks[index].allotment += 1
			count = 0
			amount -= stocks[index].price
		else:
			count += 1
		
		index += 1
		if index == size:
			index = 0
	
	return stocks
	
"""
	Checks if a network connection is available
"""	
def check_network():

    try:
        google = socket.gethostbyname("www.google.com")
        res = socket.create_connection((google, 80), 1)
        return 1
    except socket.timeout:
        pass

    return 0

"""
    Checks if a connection to the API can be established
"""
def check_connection(hosts):

    for a_host in hosts:
        try:
            requests.get(a_host, timeout=1)
            return a_host
        except (requests.ConnectionError, requests.exceptions.ReadTimeout):
            continue

    print("Connection failed")
    exit(1)


"""
    Attempts to retrieve stock data based on a ticker symbol
"""
def fetch_data_api(host, extension, ticker_symbol):
    try:
        result = requests.get(host + "/" + ticker_symbol + extension, timeout=8)
        if result.text == "Unknown symbol":
            return 0
        return result.json()["quote"]
    except (requests.exceptions.ReadTimeout, requests.exceptions.HTTPError, requests.exceptions.InvalidURL):
        print("Could not fetch the data from the API Server. We will return momentarily")
        return redirect("/")


"""
    Calculates the value change from the previous close to the current close
"""
def calc_value_change(before, after):
    if before <= after:
        return "+" + str("{:.2f}".format(after-before))
    else:
        return str("{:.2f}".format(after-before))


"""
    Calculates the percent change from the previous close to the current close
"""
def calc_percent_change(before, after):
    if before <= after:
        return "+" + str("{:.2f}".format(((after-before)/before)*100.0))
    else:
        return str("{:.2f}".format(((after - before) / before)*100.0))

"""
	Provides the current data and time
"""
def date_time():
	date = datetime.datetime.now()
	tz = time.strftime("%Z")
	tz_abb = ""

	for word in tz.split():
		tz_abb += word[0]

	date_formatted = date.strftime("%a %b %d %H:%M:%S" + " " + tz_abb + " %Y")  # time.localtime().tm_zone + " %Y")
	
	return str(date_formatted)