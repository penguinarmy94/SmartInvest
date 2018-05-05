from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from InvestMain.forms import *
from InvestMain.calculator import *

"""
	Loads the stock calculator form view
"""
def stock_calculator(request):
	stock_request = StockCalculatorForm(request.POST or None)
	
	#checks if the form had data in it
	if request.method == "POST":
		#checks if the fomr data is valid
		if stock_request.is_valid():
			request.session['data'] = stock_request.cleaned_data
			return redirect(stock_portfolio)
		else:
			return render(request, 'stock.html', {"form" : stock_request})
	
	return render(request, 'stock.html', {})

"""
	Loads the results from the stock calculator view
"""
def stock_portfolio(request):
	message_data = {}
	
	if request.method == "GET" and request.session.get('data'):
		#get all form data
		data = request.session.get('data')
		request.session['data'] = None
		
		#calculate the stock results and store them in a dictionary
		message_data['proceeds'] = compute_proceeds(data['allotment'], data['final_share_price'])
		capital_gain = compute_capital_gain(message_data['proceeds'], data['allotment'], data['initial_share_price'], data['buy_commission'], data['sell_commission'])
		message_data['capital_gain_tax'] = compute_capital_gain_tax(capital_gain, data['capital_gain_tax_rate'])
		message_data['total_purchase_price'] = compute_total_purchase_price(data['allotment'], data['initial_share_price'])
		message_data['buy_commission'] = data['buy_commission']
		message_data['sell_commission'] = data['sell_commission']
		message_data['capital_gain_tax_rate'] = data['capital_gain_tax_rate']
		message_data['allotment'] = data['allotment']
		message_data['initial_share_price'] = data['initial_share_price']
		message_data['cost'] = compute_cost(data['allotment'], data['initial_share_price'], data['buy_commission'], data['sell_commission'], message_data['capital_gain_tax'])
		message_data['net_profit'] = compute_net_profit(message_data['proceeds'], message_data['cost'])
		message_data['return_on_investment'] = compute_return_on_investment(message_data['net_profit'], message_data['cost'])
		message_data['break_even_price'] = compute_break_even_price(data['allotment'], data['initial_share_price'], data['buy_commission'], data['sell_commission'])
	else:
		return redirect(stock_calculator)
	
	return render(request, 'portfolio.html', {"message" : message_data} )

def stock_invest_options(request):
	ethical = '''Ethical Investing is based on investing in companies that are ethical in their beliefs and those believes 
				align with yours. Invest in this strategy to invest in companies based on these factors.'''
	growth = '''Growth Investing is based on investing in companies based on most recently on upward growing trends 
				Invest in this strategy if you want to go with companies recently on the rise.'''
	index = '''Index Investing is based on some form of index that do something in terms of index and are only meant to be
				defined. Invest in this option if you are interested.'''
	quality = ''' '''
	value = ''' '''
	
	ethical_stocks = []
	growth_stocks = []
	index_stocks = ["XLF", "USO", "SLV"]
	quality_stocks = []
	value_stocks = []
	
	if request.method == "GET":		
		return render(request, 'invest.html', {"ethical" : ethical, "growth" : growth, "index" : index })
	if request.method == "POST":		
		investment = InvestmentForm(request.POST or None)
		
		if investment.is_valid():
			data = investment.cleaned_data
			#for value in data:
		else:
			return redirect(stock_calculator)
				
			
		return render(request, 'invest.html', {"ethical" : ethical, "growth" : growth, "index" : index })
		
		
