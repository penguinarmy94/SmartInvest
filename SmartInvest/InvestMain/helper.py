import requests, datetime, time, socket, os, json
from myproject import settings

__file = open(os.path.join(settings.BASE_DIR,'static/json/strategies.json'))
__strategy_json = json.load(__file)
__stocks = __strategy_json["stocks"]

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

def get_strategies(data):
	strategies = []
	
	if(data["ethical_invest"] > 0):
		strategies.append("ethical_invest")
	if(data["growth_invest"] > 0):
		strategies.append("growth_invest")
	if(data["index_invest"] > 0):
		strategies.append("index_invest")
	if(data["quality_invest"] > 0):
		strategies.append("quality_invest")
	if(data["value_invest"] > 0):
		strategies.append("value_invest")
	
	return strategies

def all_stocks_to_invest(data, strategy):
	
	if(data[strategy] > 0):
		return __stocks[strategy]
	
def invest_division(data, strategies, stocks, apihost, apihost_extension):
	st_count = 0
	stock_count = {}
	
	for stock_set in stocks:
		val = strategies[st_count]
		money = data[val]
		num_of_stock = []
		stock_data = []
		count = 0
		
		for stock in stock_set:
			stock_data.append(fetch_data_api(apihost, apihost_extension, stock))
			num_of_stock.append(0)
			count = count + 1
			
		no_more_stocks = 0
		i = 0
		while i < len(stock_data):
			if (stock_data[i]["close"] <= money):
				num_of_stock[i] = num_of_stock[i] + 1;
				no_more_stock = 0
				money -= stock_data[i]["close"]
			else:
				no_more_stocks = no_more_stocks + 1
		
			if(i == len(stock_data)-1):
		
				if (money == 0 or no_more_stocks >= len(stock_data)):
					break
				else:
					i = -1
			i += 1
		stock_count[val] = num_of_stock
		st_count += 1
	
	return stock_count

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
        result = requests.get(host + "/" + ticker_symbol + extension, timeout=1)
        if result.text == "Unknown symbol":
            return 0
        return result.json()["quote"]
    except (requests.exceptions.ReadTimeout, requests.exceptions.HTTPError, requests.exceptions.InvalidURL):
        print("Count not fetch the data from the API Server. We will return momentarily")
        exit(1)


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


def date_time():
	date = datetime.datetime.now()
	tz = time.strftime("%Z")
	tz_abb = ""

	for word in tz.split():
		tz_abb += word[0]

	date_formatted = date.strftime("%a %b %d %H:%M:%S" + " " + tz_abb + " %Y")  # time.localtime().tm_zone + " %Y")
	
	return str(date_formatted)
	
"""
    Prints the results of the stock data
"""
def print_results(name, symbol, price, change, percent_change):
    date = datetime.datetime.now()
    tz = time.strftime("%Z")
    tz_abb = ""

    for word in tz.split():
        tz_abb += word[0]

    date_formatted = date.strftime("%a %b %d %H:%M:%S" + " " + tz_abb + " %Y")  # time.localtime().tm_zone + " %Y")
    init = "\nStock Results\n-------------------------------------------------\n"
    print("%s%s\n%s(%s)\n$%.2f %s (%s%%)\n" %(init,date_formatted,name,symbol,price,change,percent_change))