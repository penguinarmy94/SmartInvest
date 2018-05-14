
class Stock:
	symbol = ""
	name = ""
	allotment = 0
	price = 0
	full_price = 0
	
	def __init__(self, symbol, shares):
		self.symbol = symbol
		self.allotment = shares